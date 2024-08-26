from functools import wraps
from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from .form import CustomLoginForm, CustomUserCreationForm,OTPVerificationForm
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .models import CustomUser,UploadedFile
from .form import FileUploadForm
from rest_framework import generics, permissions
from .serializers import UploadedFileSerializer
# from two_factor.views import LoginView
from django.contrib.auth import authenticate
from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model




def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
   

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        # Authenticate user
        user = form.get_user()
        email_device, created = EmailDevice.objects.get_or_create(user=user)

        # Generate OTP
        email_device.generate_token()
        email_device.save()

        # Send OTP via email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {email_device.token}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        # Redirect to OTP verification page
        self.request.session['pre_2fa_user_id'] = user.id
        return redirect('verify_otp')

class OTPVerificationView(LoginView):
    template_name = 'verify_otp.html'
    form_class = OTPVerificationForm

    def get_form_kwargs(self):
        # Use this method to add request to form kwargs if needed
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        user_id = self.request.session.get('pre_2fa_user_id')
        if not user_id:
            return redirect('login')

        user = User.objects.get(id=user_id)
        email_device = EmailDevice.objects.get(user=user)

        if email_device.verify_token(form.cleaned_data['otp']):
            login(self.request, user)
            del self.request.session['pre_2fa_user_id']
            return redirect(reverse_lazy('upload_books'))
        else:
            form.add_error('otp', 'Invalid OTP')
            return self.form_invalid(form)
        

def authors_and_sellers(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        users = CustomUser.objects.filter(username__icontains=query, public_visibility=True)
    else:
        users = CustomUser.objects.filter(public_visibility=True)
    
    return render(request, 'authors_and_sellers.html', {'users': users})


def upload_books(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('view_uploaded_files')
    else:
        form = FileUploadForm()
    return render(request, 'upload_books.html', {'form': form})

def user_has_uploaded_files(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if UploadedFile.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('upload_books')  # Redirect to Upload Books if no files
    return _wrapped_view

@user_has_uploaded_files
def view_uploaded_files(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'view_uploaded_files.html', {'files': files})

class UserUploadedFileListView(generics.ListAPIView):
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)



def send_otp(request, user):
    device = user.get_or_create_email_otp_device()
    if device.confirmed:
        device.generate_token()
        device.save()
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {device.token}.',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    # Instead of redirecting, return a message
    return JsonResponse({'message': 'OTP sent. Please verify by sending a POST request to /auth/verify-otp/ with your OTP.'})


User = get_user_model()

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        username = request.POST.get("username")

        if not otp or not username:
            return JsonResponse({'error': 'OTP and username are required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        device = user.get_or_create_email_otp_device()

        if device.verify_token(otp):
            device.confirmed = True
            device.save()

            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Return the tokens in a JSON response
            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        else:
            # Return an error message in JSON response if OTP is invalid
            return JsonResponse({
                'error': 'Invalid OTP'
            }, status=400)
    
    # Return an error if the method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=405)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user is not None:
            # Send OTP email
            return send_otp(request, user)
        return response
    