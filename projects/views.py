from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Block, Project, Section
from .serializers import (
    BlockSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
    SectionSerializer,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ProjectCreateSerializer
        return ProjectSerializer

    def destroy(self, request, *args, **kwargs):
        if Section.objects.filter(project=kwargs["pk"]).count() > 0:
            return Response(
                {"error": "Project has sections associated with it"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            user = self.request.user
            project = serializer.save(user=user)
            section = Section.objects.create(
                user=user, project=project, title=f"{project.title} Cross Section"
            )
            return Response(
                {
                    "project": ProjectSerializer(
                        project, context=self.get_serializer_context()
                    ).data,
                    "new_section_id": section.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AllProjectsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlockViewSet(ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def create_empty_section(self, project, user):
        section_count = Section.objects.filter(project=project).count() + 1
        title = f"{project.title} S{section_count}"

        section = Section.objects.create(
            user=user,
            project=project,
            title=title,
        )
        return section

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["get"],
        url_path="project-sections",
        permission_classes=[IsAuthenticated],
    )
    def get_project_sections(self, request, pk=None):
        # Ottieni il progetto specificato dall'ID passato
        project = Project.objects.filter(pk=pk, user=request.user).first()

        if not project:
            return Response(
                {"error": "Project not found or not authorized"}, status=404
            )

        # Ottieni le sezioni relative al progetto
        sections = Section.objects.filter(project=project)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=200)
