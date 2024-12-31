from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count, Q

from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.exam_batch.model import ExamBatch
from admin_panel.exam_batch.serializer import ExamBatchResponseSerializer
from admin_panel.exam_employee.model import ExamEmployee, ExamEmployeeRole
from admin_panel.exam_employee.serializer import ExamEmployeeAssignmentSerializer, ExamEmployeeResponseSerializer, EmployeeBatchStatisticsSerializer
from admin_panel.exam_paper.model import ExamPaper, ExamStudentEvaluatorMappingStatus
from admin_panel.exams.model import Exam
from admin_panel.users.models.employee import Employee



class ExamEmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing employee assignments to exams
    """
    queryset = ExamEmployee.objects.all()
    serializer_class = ExamEmployeeResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam_batch', 'role']

    @swagger_auto_schema(
        tags=['Exam Employees'],
        operation_summary="Assign employees to exam",
        operation_description="Assign multiple employees to an exam with a specific role",
        request_body=ExamEmployeeAssignmentSerializer,
        responses={
            201: ExamEmployeeResponseSerializer(many=True),
            400: "Bad Request - Invalid data or validation error",
            404: "Not Found - Exam does not exist"
        }
    )
    @action(detail=False, methods=['post'], url_path='assign')
    @transaction.atomic
    def assign_employees(self, request):
        serializer = ExamEmployeeAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        exam_batch = get_object_or_404(ExamBatch, id=serializer.validated_data['exam_batch'])
        employee_ids = serializer.validated_data['employee_ids']
        role = serializer.validated_data['role']
        
        # Delete existing assignments for this role
        ExamEmployee.objects.filter(exam_batch=exam_batch, role=role).delete()
        
        # Create new assignments
        new_assignments = []
        for employee_id in employee_ids:
            employee = Employee.objects.get(id=employee_id)
            assignment = ExamEmployee.objects.create(
                exam_batch=exam_batch,
                employee=employee,
                role=role,
                organization=exam_batch.organization
            )
            new_assignments.append(assignment)
        
        response_serializer = ExamEmployeeResponseSerializer(
            new_assignments, 
            many=True
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        tags=['Exam Employees'],
        operation_summary="Get exam employees by role",
        operation_description="Get list of employees assigned to an exam by role",
        manual_parameters=[
            openapi.Parameter(
                'exam_batch',
                openapi.IN_QUERY,
                description="UUID of the exam batch",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'role',
                openapi.IN_QUERY,
                description="Role of the employees (EVALUATOR, MODERATOR, SCANNER)",
                type=openapi.TYPE_STRING,
                required=True,
                enum=[choice[0] for choice in ExamEmployeeRole.choices]
            )
        ],
        responses={
            200: ExamEmployeeResponseSerializer(many=True),
            400: "Bad Request - Missing or invalid parameters",
            404: "Not Found - Exam does not exist"
        }
    )
    @action(detail=False, methods=['get'], url_path='by-role')
    def get_employees_by_role(self, request):
        exam_batch = request.query_params.get('exam_batch')
        role = request.query_params.get('role')

        if not exam_batch or not role:
            return Response(
                {"error": "Both exam_batch and role are required query parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        exam_batch = get_object_or_404(ExamBatch, id=exam_batch)
        
        try:
            assignments = ExamEmployee.objects.filter(
                exam_batch=exam_batch,
                role=role.upper()
            )
        except ValueError:
            return Response(
                {"error": f"Invalid role. Must be one of {[choice[0] for choice in ExamEmployeeRole.choices]}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(assignments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Exam Employees'],
        operation_summary="Get exam batches for employee",
        operation_description="Get all exam batches assigned to an employee with paper statistics",
        manual_parameters=[
            openapi.Parameter(
                'employee_id',
                openapi.IN_QUERY,
                description="UUID of the employee",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: EmployeeBatchStatisticsSerializer(many=True),
            400: "Bad Request - Missing employee_id",
            404: "Not Found - Employee does not exist"
        }
    )
    @action(detail=False, methods=['get'], url_path='employee-batches')
    def get_employee_batches(self, request):
        employee_id = request.query_params.get('employee_id')
        
        if not employee_id:
            return Response(
                {"error": "employee_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all assignments for the employee
        exam_assignments = self.queryset.filter(
            employee_id=employee_id
        ).select_related('exam_batch')

        response_data = []
        for assignment in exam_assignments:
            exam_batch = assignment.exam_batch
            
            # Get paper statistics for this exam batch
            paper_stats = ExamPaper.objects.filter(
                exam=exam_batch.exam,
                employee_id=employee_id
            ).aggregate(
                total=Count('id'),
                evaluated=Count('id', filter=Q(status=ExamStudentEvaluatorMappingStatus.FINISHED)),
                in_progress=Count('id', filter=Q(status=ExamStudentEvaluatorMappingStatus.IN_PROGRESS)),
                not_started=Count('id', filter=Q(status=ExamStudentEvaluatorMappingStatus.NOT_STARTED))
            )

            # Serialize exam batch data
            response_data.append({
                'exam_batch': ExamBatchResponseSerializer(exam_batch).data,
                'paper_statistics': paper_stats,
                'role': assignment.role
            })

        return Response(response_data)