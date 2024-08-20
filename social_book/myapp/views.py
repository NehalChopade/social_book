from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from .form import CustomLoginForm, CustomUserCreationForm
from django.contrib.auth import views as auth_views
from .models import CustomUser,UploadedFile
from .form import FileUploadForm

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
   

class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm

    def get_redirect_url(self):
        # Redirect to 'upload-books/' after successful login
        return reverse_lazy('upload_books')

# def authors_and_sellers(request):
#     query = request.GET.get('q', '')
#     users = CustomUser.objects.filter(public_visibility=True)
#     if query:
#         users = users.filter(email_icontains=query)
#     return render(request, 'authors_and_sellers.html', {'users': users, 'query': query})

# def authors_and_sellers(request):
#     users = CustomUser.objects.filter(public_visibility=True)
#     return render(request, 'authors_and_sellers.html', {'users': users})

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

def view_uploaded_files(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'view_uploaded_files.html', {'files': files})


