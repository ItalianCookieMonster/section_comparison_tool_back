from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('blocks', views.BlockViewSet)
router.register('sections', views.SectionViewSet)


urlpatterns = [
    path('admin/projects/', views.AllProjectsView.as_view(), name='all-projects'),
    path('projects/<int:pk>/sections/', views.SectionViewSet.as_view({'get': 'get_project_sections'}), name='project-sections'),
] + router.urls

