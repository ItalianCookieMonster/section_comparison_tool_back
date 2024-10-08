from django.urls import path
from rest_framework import routers
from .views import AccountViewSet


router = routers.DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')


urlpatterns = router.urls