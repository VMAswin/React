# users/views.py
from rest_framework import viewsets
from .models import Customuser
from rest_framework import generics
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.conf import settings
import string
import random


class UserViewSet(viewsets.ModelViewSet):
    queryset = Customuser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        random_password = ''.join(random.choices(string.digits, k=6))
        user.set_password(random_password)
        user.save()
        send_mail(
            'Welcome!',
            'Thank you for registering.'+random_password,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


