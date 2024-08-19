from django.contrib import admin
from .models import (CustomUser)
model_tuple=(CustomUser)
admin.site.register(model_tuple)

