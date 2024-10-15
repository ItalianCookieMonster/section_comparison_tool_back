from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .calculation_service import SectionCalculationsService
from .models import Block, Project, Section, SectionBlock
from .serializers import (
    BlockSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
    SectionBlockCreateSerializer,
    SectionBlockDetailSerializer,
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

            return Response(
                {
                    "project": ProjectSerializer(
                        project, context=self.get_serializer_context()
                    ).data
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

    def create(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")

        if not project_id:
            return Response(
                {"error": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            project = Project.objects.get(id=project_id, user=request.user)

            section = Section.objects.create(
                project=project,
                user=request.user,
                title=f"{project.title} Section",
            )

            return Response(
                SectionSerializer(section).data, status=status.HTTP_201_CREATED
            )

        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found or not authorized"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["get"],
        url_path="project-sections",
        permission_classes=[IsAuthenticated],
    )
    def get_project_sections(self, request, pk=None):
        project = Project.objects.filter(pk=pk, user=request.user).first()

        if not project:
            return Response(
                {"error": "Project not found or not authorized"}, status=404
            )

        sections = Section.objects.filter(project=project)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"], url_path="calculate-all")
    def calculate_all_metrics(self, request, pk=None):
        try:
            calculation_service = SectionCalculationsService(section_id=pk)

            results = calculation_service.perform_all_calculations()

            section = Section.objects.get(id=pk)
            section.height = results["height"]
            section.face_area = results["face_area"]
            section.concrete_volume = results[
                "concrete_volume"
            ]  # Salva anche il volume
            section.save()

            return Response(
                {
                    "message": "Calculated all metrics successfully",
                    "section": SectionSerializer(section).data,
                    "calculated_data": results,
                },
                status=status.HTTP_200_OK,
            )

        except Section.DoesNotExist:
            return Response(
                {"error": "Section not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SectionBlockViewSet(viewsets.ModelViewSet):
    queryset = SectionBlock.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return SectionBlockCreateSerializer
        return SectionBlockDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        section_id = self.request.query_params.get("section_id")
        print("section_id", section_id)
        if section_id:
            queryset = queryset.filter(section_id=section_id)

        if not queryset.exists():
            return queryset.none()

        return queryset

    def perform_create(self, serializer):
        if serializer.is_valid():
            section = serializer.validated_data.get("section")
            block = serializer.validated_data.get("block")
            quantity = serializer.validated_data.get("quantity")

            existing_section_block = SectionBlock.objects.filter(
                section=section, block=block
            ).first()

            if existing_section_block:
                existing_section_block.quantity += quantity
                existing_section_block.save()
                serializer.instance = existing_section_block
            else:
                serializer.save()

    @action(
        detail=False,
        methods=["delete"],
        url_path="(?P<section_id>[^/.]+)/blocks/(?P<block_id>[^/.]+)",
    )
    def delete_section_block(self, request, section_id=None, block_id=None):
        try:
            section_block = get_object_or_404(
                SectionBlock, section_id=section_id, block_id=block_id
            )
            section_block.delete()
            return Response(
                {"message": "Section block deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
