from django.db import models
from django.contrib.auth.models import AbstractUser


class Customuser(AbstractUser):
    user_type=models.IntegerField(default=0)

class UserProfile(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=25)
    department=models.CharField(max_length=25)
    Image=models.ImageField(upload_to='Dimage/',null=True,blank=True)
    certificate=models.FileField(upload_to='files/',blank=True,null=True)

class Department(models.Model):
    Department_name = models.CharField(max_length=25)
    Description = models.CharField(max_length=25)

class Trainer(models.Model):
    Trainer_name = models.CharField(max_length=25)
    Date = models.DateField()
    status =models.CharField(max_length=20)