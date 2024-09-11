from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('blocks', views.BlockViewSet)
router.register('sections', views.SectionViewSet)


urlpatterns = router.urls

