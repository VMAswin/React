# users/serializers.py
import random
import string
from .models import Customuser,UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('certificate','profile','department','phone_number')

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customuser
        fields = ('username', 'email','user_type')

    # def create(self, validated_data):
    #     user = Customuser.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         # password=str(random.randint(100000,999999))
            
    #     )
    #     return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
