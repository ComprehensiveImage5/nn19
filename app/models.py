from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.
class CheckIn(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2)
    datetime = models.DateTimeField()