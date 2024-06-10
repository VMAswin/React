

from .models import Customuser,UserProfile,Department,Trainer,Projects,Trainee,Leave
from rest_framework import serializers
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('certificate','profile','department','phone_number')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customuser
        fields = ('username', 'email','user_type')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('Department_name','Description')

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class AllocateprojectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Projects
        fields = '__all__'

class TraineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainee
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'        

       
  
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__' 

class USerializer(serializers.Serializer):
    id = serializers.IntegerField()

   

