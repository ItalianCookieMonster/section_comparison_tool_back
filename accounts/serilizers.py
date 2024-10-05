from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'role', 'company_name', 'phone', 'user',]
        extra_kwargs = {'user': {'read_only': True}}


