from django.shortcuts import render,redirect
from django.contrib.auth import login
from .form import CustomLoginForm, CustomUserCreationForm
from django.contrib.auth import views as auth_views
from .models import CustomUser


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


def authors_and_sellers(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(public_visibility=True)
    if query:
        users = users.filter(email_icontains=query)
    return render(request, 'authors_and_sellers.html', {'users': users, 'query': query})


