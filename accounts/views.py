from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Account
from .serilizers import AccountSerializer

# Create your views here.


class AccountViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated] 
        
        
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        (account, created) = Account.objects.get_or_create(user=request.user)

        if(request.method == 'GET'):
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        elif(request.method == 'PUT'):
            serializer = AccountSerializer(account, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    