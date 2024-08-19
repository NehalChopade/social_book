from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
# Create your models here.

class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    birth_year = models.PositiveIntegerField(null=True,blank=True)
    address = models.CharField(max_length=225,blank=True)

    @property
    def age(self):
        return date.today().year - self.birth_year