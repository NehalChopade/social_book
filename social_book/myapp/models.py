from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django_otp.models import Device
from django_otp.plugins.otp_email.models import EmailDevice

# Create your models here.

class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    birth_year = models.PositiveIntegerField(null=True,blank=True)
    address = models.CharField(max_length=225,blank=True)

    @property
    
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None
    
    def get_or_create_email_otp_device(self):
        device, created = EmailDevice.objects.get_or_create(user=self, name='default')
        return device
    
# class UploadedFile(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='uploads/', validators=[
#         FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg'])
#     ])
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     visibility = models.BooleanField(default=True)
#     cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     year_published = models.PositiveIntegerField(null=True, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title   
class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'jpeg', 'jpg'])
    ])
    cover_image = models.ImageField(upload_to='cover_images/', validators=[
        FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])
    ], null=True, blank=True)  # New field for the cover image
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    visibility = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    year_published = models.PositiveIntegerField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 