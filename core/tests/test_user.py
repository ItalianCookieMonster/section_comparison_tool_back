import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from core.models import User


@pytest.mark.django_db
class TestCreateUser(TestCase):
    
    def test_user_registration(self):
        """
            Given a user registration request
            When the data is correct
            Then it should return a response with the user data
        """
        client = APIClient()
        url = '/api/v1/auth/users/'
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'passwordTest',
            'full_name': 'Test User',
            'verified': True
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'email' in response.data
        

    def test_user_registration_with_incorrect_password(self):
        """
            Given a user registration request
            When the password is too common
            Then it should return a 400 status code error
            And a meaningful error message
        """
        client = APIClient()
        url = '/api/v1/auth/users/'
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password', 
            'full_name': 'Test User',
            'verified': True
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_user_registration_missing_data(self):
        """
            Given a user registration an user registration request
            When the data is missing
            Then it should return a 400 status code error
            And a meaningful error message
        """
        client = APIClient()
        url = '/api/v1/auth/users/'
        data = {
            'email': 'testuser@example.com',
            'password': 'passwordTest', 
            'full_name': 'Test User',
            'verified': True
        }
        response = client.post(url, data)
        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data



@pytest.mark.django_db
class TestAuthUser(TestCase):
    
    def test_auth_user_success(self):
        """
            Given a user registration request
            When the data is correct
            Then it should return a response with status code 201
            And the user token
        """
        User.objects.create_user(username='testuser', password='passwordTest')

        client = APIClient()
        url = '/api/v1/auth/jwt/create/'
        data = {
            'username': 'testuser',
            'password': 'passwordTest',
        }
        
        response = client.post(url, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    
    def test_auth_user_with_incorrect_password(self):
        """
            Given a user registration request
            When the password is too common
            Then it should return a 400 status code error
            And a meaningful error message
        """
        User.objects.create_user(username='testuser', password='passwordTest')

        client = APIClient()
        url = '/api/v1/auth/jwt/create/'
        data = {
            'username': 'testuser',
            'password': 'password',
        }
        
        response = client.post(url, data)
        print (response.data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'detail' in response.data
    