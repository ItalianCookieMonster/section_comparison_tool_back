from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
import pytest

@pytest.mark.django_db
class TestCreateCollection(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        
    
    def test_create_project(self):
        """
            Given an anonymous user
            When creating a project
            Then should receive a 401 status code
        """
        
        client = APIClient()
        response = client.post('/api/v1/projects/', {
            'title': 'Test Project',
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_project_as_user(self):
        """
            Given a user
            When creating a project
            Then should receive a 201 status code
        """
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post('/api/v1/projects/',{'title': 'Test Project',
        'user': self.user.id,
        'company_name': 'Test Company',
        'concrete_density': 2400,
        'currency': 'EUR',
        'concrete_cost': 100,
        'labour_cost': 50,
        'avg_truck_capacity': 20,
        'infill_density': 1800,
        'infill_cost': 30,
        'avg_truck_cost': 150,
        'avg_production_time': 10,
        'royalty': 5,
        'pur_per_year': 1000,
        'cem_content': 350,
        'address': '123 Test St',
        'zip_code': '12345',
        'language': 'en'
        })
        
        assert response.status_code == status.HTTP_201_CREATED    
        
    def test_retrieve_project(self):
        project = {
            'company_name': 'Test Company',
        'concrete_density': 2400,
        'currency': 'EUR',
        'concrete_cost': 100,
        'labour_cost': 50,
        'avg_truck_capacity': 20,
        'infill_density': 1800,
        'infill_cost': 30,
        'avg_truck_cost': 150,
        'avg_production_time': 10,
        'royalty': 5,
        'pur_per_year': 1000,
        'cem_content': 350,
        'address': '123 Test St',
        'zip_code': '12345',
        'language': 'en'
        }
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/projects/1/', project)
        assert response.status_code == status.HTTP_200_OK
    