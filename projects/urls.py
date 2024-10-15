from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("projects", views.ProjectViewSet)
router.register("blocks", views.BlockViewSet)
router.register("sections", views.SectionViewSet)
router.register("sectionblocks", views.SectionBlockViewSet)

urlpatterns = [
    path("admin/projects/", views.AllProjectsView.as_view(), name="all-projects"),
    path(
        "projects/<int:pk>/sections/",
        views.SectionViewSet.as_view({"get": "get_project_sections"}),
        name="project-sections",
    ),
    path(
        "sectionblocks/<int:section_id>/blocks/<int:block_id>/",
        views.SectionBlockViewSet.as_view({"delete": "delete_section_block"}),
    ),
    path(
        "sections/<int:pk>/calculate-all/",
        views.SectionViewSet.as_view({"post": "calculate_all_metrics"}),
    ),
] + router.urls
