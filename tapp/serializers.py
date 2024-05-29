from rest_framework import serializers
from .models import Customuser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Customuser.objects.create_user(**validated_data)
        return user
        

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = '__all__'

# class RentalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rental
#         fields = '__all__'

# class PurchaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Purchase
#         fields = '__all__'