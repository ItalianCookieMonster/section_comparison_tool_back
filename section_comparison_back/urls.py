
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Section Comparison Admin"
admin.site.site_title = "Section Comparison Admin Portal"
admin.site.index_title = "Welcome to Section Comparison Portal"

API_URL = 'api/'
VERSION = 'v1/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{API_URL}{VERSION}auth/', include('djoser.urls')),
    path(f'{API_URL}{VERSION}auth/', include('djoser.urls.jwt')),

    path(f'{API_URL}{VERSION}accounts/', include('accounts.urls')),
    path(f'{API_URL}{VERSION}', include('projects.urls')),
]
