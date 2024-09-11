from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('projects', views.ProjectViewSet)
router.register('blocks', views.BlockViewSet)
router.register('sections', views.SectionViewSet)


urlpatterns = router.urls


# urlpatterns = [
#     path('projects/', views.ProjectList.as_view()),
#     path('projects/<int:pk>/', views.ProjectDetail.as_view()),
#     path('blocks/', views.BlockList.as_view()),
#     path('blocks/<int:pk>/', views.BlockDetail.as_view()),
#     path('sections/', views.SectionList.as_view()),
#     path('sections/<int:pk>/', views.SectionDetail.as_view()),
# ]
