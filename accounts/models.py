from django.db import models
from django.conf import settings

class Account(models.Model):
    role = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=100)
    company_contact = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    
    def __str__(self):
        return self.company_name