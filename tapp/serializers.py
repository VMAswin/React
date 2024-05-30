# users/serializers.py
import random
import string
from .models import Customuser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ('username', 'email')

    def create(self, validated_data):
        user = Customuser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            # password=str(random.randint(100000,999999))
            
        )
        return user
