from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from admin_panel.exam_batch.model import (
    ExamBatch,
    ExamBatchSettings,
    InternetBasedSettings,
    PaperBasedSettings,
    EvaluatorSettings,
    ModeratorSettings,
    ScannerSettings,
    SelectionCriteria,
)
from admin_panel.exam_batch.serializer import (
    ExamBatchCreateSerializer,
    ExamBatchResponseSerializer,
    ExamBatchSettingsRequestSerializer,
)
from admin_panel.exam_batch_student.model import ExamStudent
from django.db.models import Count, Q
from drf_yasg import openapi
from admin_panel.exam_paper.model import ExamPaper, ExamStudentEvaluatorMappingStatus
from admin_panel.exam_employee.model import ExamEmployee


class ExamBatchViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing exam-batch relationships.
    """
    queryset = ExamBatch.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam', 'batch']

    def get_serializer_class(self):
        if self.action == 'create':
            return ExamBatchCreateSerializer
        return ExamBatchResponseSerializer

    @swagger_auto_schema(
        tags=['Exam Batches'],
        operation_summary="Add batch to exam",
        operation_description="Add a batch to an exam and optionally clone its students",
        request_body=ExamBatchCreateSerializer,
        responses={
            201: ExamBatchResponseSerializer,
            400: "Bad Request - Invalid data or validation error"
        }
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        clone_students = request.data.pop('clone_students', True)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exam_batch = serializer.save()

        if clone_students:
            batch_students = exam_batch.batch.student.all()
            exam_students = []
            
            for student in batch_students:
                # Check if student already has 2 batches for this exam
                existing_count = ExamStudent.objects.filter(
                    student=student,
                    exam_batch__exam=exam_batch.exam
                ).count()
                
                if existing_count < 2:
                    exam_students.append(
                        ExamStudent(
                            exam_batch=exam_batch,
                            student=student
                        )
                    )
            
            if exam_students:
                ExamStudent.objects.bulk_create(exam_students)

        response_serializer = ExamBatchResponseSerializer(exam_batch)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        tags=['Exam Batches'],
        operation_summary="Update exam batch settings",
        operation_description="Update all settings for an exam batch including mode specific settings",
        request_body=ExamBatchSettingsRequestSerializer,
        responses={
            200: "Settings updated successfully",
            400: "Bad Request - Invalid data or validation error",
            404: "Not Found - Exam batch does not exist"
        }
    )
    @action(detail=True, methods=['put'], url_path='settings')
    @transaction.atomic
    def update_settings(self, request, pk=None):
        exam_batch = self.get_object()
        
        # Initialize serializer with exam_batch context
        serializer = ExamBatchSettingsRequestSerializer(
            data=request.data,
            context={'exam_batch': exam_batch}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Update exam batch schedule
        for field in ['start_date', 'end_date', 'start_time', 'end_time',
                     'evaluation_start_date', 'evaluation_end_date',
                     'evaluation_start_time', 'evaluation_end_time']:
            if field in data:
                setattr(exam_batch, field, data[field])
        exam_batch.save()

        # Update common settings
        if common_settings := data.get('common_settings'):
            ExamBatchSettings.objects.update_or_create(
                exam_batch=exam_batch,
                defaults=common_settings
            )

        # Update mode specific settings
        if exam_batch.mode in ['INTERNET_BASED', 'INTERNET_BASED_HYBRID']:
            if internet_settings := data.get('internet_settings'):
                InternetBasedSettings.objects.update_or_create(
                    exam_batch=exam_batch,
                    defaults=internet_settings
                )

        if exam_batch.mode in ['PAPER_BASED_OSM', 'PAPER_BASED_OMR', 'PAPER_BASED_ATTACHMENT']:
            if paper_settings := data.get('paper_settings'):
                PaperBasedSettings.objects.update_or_create(
                    exam_batch=exam_batch,
                    defaults=paper_settings
                )

            # Update evaluation related settings
            if evaluator_settings := data.get('evaluator_settings'):
                EvaluatorSettings.objects.update_or_create(
                    exam_batch=exam_batch,
                    defaults=evaluator_settings
                )

            if moderator_settings := data.get('moderator_settings'):
                ModeratorSettings.objects.update_or_create(
                    exam_batch=exam_batch,
                    defaults=moderator_settings
                )

            if scanner_settings := data.get('scanner_settings'):
                ScannerSettings.objects.update_or_create(
                    exam_batch=exam_batch,
                    defaults=scanner_settings
                )

        # Update selection criteria
        if selection_criteria := data.get('selection_criteria'):
            SelectionCriteria.objects.update_or_create(
                exam_batch=exam_batch,
                defaults=selection_criteria
            )

        return Response({"message": "Settings updated successfully"})

    @swagger_auto_schema(
        tags=['Exam Batches'],
        operation_summary="List exam batches",
        operation_description="Get a list of all exam batches with optional filtering by exam and batch",
        responses={
            200: ExamBatchResponseSerializer(many=True),
            400: "Bad Request - Invalid filter parameters"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Exam Batches'],
        operation_summary="Get exam batch details",
        operation_description="Retrieve detailed information about a specific exam batch",
        responses={
            200: ExamBatchResponseSerializer,
            404: "Not Found - Exam batch does not exist"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
