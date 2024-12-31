from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.exam_employee.model import ExamEmployee, ExamEmployeeRole
from admin_panel.exam_employee.serializer import ExamEmployeeAssignmentSerializer, ExamEmployeeResponseSerializer
from admin_panel.exam_paper.model import ExamPaper
from admin_panel.exam_paper.serializer import ExamPaperResponseSerializer
from admin_panel.exams.model import Exam
from admin_panel.users.models.employee import Employee



class ExamPaperViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing exam papers
    """
    queryset = ExamPaper.objects.all()
    serializer_class = ExamPaperResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'employee']


    @swagger_auto_schema(
        tags=['Exam Papers'],
    )
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Exam Papers'],
    )
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Exam Papers'],
    )
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Exam Papers'],
    )
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Exam Papers'],
    )
    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Exam Papers'],
    )
    def retrieve(self, request, *args, **kwargs):
        super().retrieve(request, *args, **kwargs)
    