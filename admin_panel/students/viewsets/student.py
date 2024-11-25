from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from admin_panel.models import Student
from admin_panel.students.serializers.student import StudentResponseSerializer, StudentSerializer


class StudentViewset(viewsets.ModelViewSet):
    """
    API endpoints for managing students in the system.
    Supports searching by first_name and last_name, and filtering on all fields.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filterset_fields = '__all__'

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StudentResponseSerializer
        return StudentSerializer

    @swagger_auto_schema(
        tags=['Students'],
        operation_summary="List students",
        operation_description="Returns a list of all students. Supports searching by first_name and last_name, and filtering on all fields.",
        responses={200: StudentResponseSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by first_name or last_name",
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Students'],
        operation_summary="Create student",
        operation_description="Create a new student record",
        request_body=StudentSerializer,
        responses={201: StudentSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Students'],
        operation_summary="Get student details",
        operation_description="Retrieve details of a specific student by ID",
        responses={200: StudentResponseSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Students'],
        operation_summary="Update student",
        operation_description="Update all fields of a specific student",
        request_body=StudentSerializer,
        responses={200: StudentSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Students'],
        operation_summary="Partial update student",
        operation_description="Update specific fields of a student",
        request_body=StudentSerializer,
        responses={200: StudentSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Students'],
        operation_summary="Delete student",
        operation_description="Remove a student record",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
