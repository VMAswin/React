from django.db import models
from django.contrib.auth.models import AbstractUser


class Customuser(AbstractUser):
    user_type=models.IntegerField(default=0)
    is_approved = models.IntegerField(default=0)
    
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

class Projects(models.Model):
    project_name = models.CharField(max_length=25)
    start_date = models.DateField()
    end_date = models.DateField()

class Trainee(models.Model):
    Trainee_name = models.CharField(max_length=25)
    Date = models.DateField()
    status =models.CharField(max_length=20)
    trainee = models.ForeignKey(Customuser,on_delete=models.CASCADE,null=True)

class Leave(models.Model):
    name = models.CharField(max_length=25)
    role = models.CharField(max_length=25)
    start_date = models.DateField()
    end_date = models.DateField()

class Uploadprojects(models.Model):
    project_name = models.CharField(max_length=25)
    date = models.DateField()
    file=models.FileField(upload_to='files/',blank=True,null=True)

class Allocation(models.Model):
    trainee_name = models.CharField(max_length=25)
    trainer_name = models.CharField(max_length=25)
    

class Notifications(models.Model):
    Notification = models.CharField(max_length=25)


