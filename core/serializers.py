from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer  as BaseUserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Account
from .models import User

User = get_user_model() 


# class UserCreateSerializer(BaseUserCreateSerializer):

#     class Meta(BaseUserCreateSerializer.Meta):
#         model = User
#         fields = ['id', 'username', 'email', 'password', 'full_name', 'verified']

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'verified', 'is_staff']


class UserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    company_name = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    
    confirm_password = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User 
        fields = ('id', 'username', 'password', 'email', 'full_name', 'verified', 'role', 'company_name', 'phone', 'confirm_password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        
        role = validated_data.pop('role')
        company_name = validated_data.pop('company_name')
        phone = validated_data.pop('phone')

        user = super().create(validated_data)
        
        Account.objects.create(
            user=user,
            role=role,
            company_name=company_name,
            phone=phone
        )

        return user
        
        