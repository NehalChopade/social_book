"""
URL configuration for social_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from myapp.views import UserUploadedFileListView, register, CustomLoginView, authors_and_sellers, upload_books, view_uploaded_files

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register,name='register'),
    path('', CustomLoginView.as_view(), name='login'),
    path('authors-and-sellers/', authors_and_sellers, name='authors_and_sellers'),
    path('upload-books/', upload_books, name='upload_books'),
    path('view-uploaded-files/', view_uploaded_files, name='view_uploaded_files'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('my-files/', UserUploadedFileListView.as_view(), name='user-files'),
    
]

