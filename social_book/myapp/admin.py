from django.contrib import admin
from .models import (CustomUser, UploadedFile)
model_tuple=(CustomUser, UploadedFile)
admin.site.register(model_tuple)

