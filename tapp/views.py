from rest_framework import viewsets
from .models import Customuser
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
import random
import string

class UserViewSet(viewsets.ModelViewSet):
    queryset = Customuser.objects.all()
    serializer_class = UserSerializer

# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class RentalViewSet(viewsets.ModelViewSet):
#     queryset = Rental.objects.all()
#     serializer_class = RentalSerializer

# class PurchaseViewSet(viewsets.ModelViewSet):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            random_password = ''.join(random.choices(string.digits, k=6))
            user.set_password(random_password)
            user.save()
            
            send_mail(
                'Library Management System Registration',
                f'Your registration is successful. Your password is: {random_password}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



