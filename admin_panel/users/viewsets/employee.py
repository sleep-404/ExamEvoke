from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from admin_panel.users.models.employee import Employee, EmployeeRole
from admin_panel.users.serializers.employee import EmployeeResponseSerializer, EmployeeSerializer


from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from admin_panel.users.models.employee import Employee, EmployeeRole
from admin_panel.users.serializers.employee import EmployeeResponseSerializer, EmployeeSerializer



class EmployeeViewset(viewsets.ModelViewSet):
    """
    API endpoints for managing employees in the system.
    Supports searching by first_name and last_name, and filtering on all fields.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filterset_fields = '__all__'

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EmployeeResponseSerializer
        return EmployeeSerializer

    @swagger_auto_schema(
        tags=['Employees'],
        operation_summary="List employees",
        operation_description="Returns a list of all employees. Supports searching by first_name and last_name, and filtering on all fields.",
        responses={200: EmployeeResponseSerializer(many=True)},
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
        tags=['Employees'],
        operation_summary="Create employee",
        operation_description="Create a new employee record",
        request_body=EmployeeSerializer,
        responses={201: EmployeeSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Employees'],
        operation_summary="Get employee details",
        operation_description="Retrieve details of a specific employee by ID",
        responses={200: EmployeeResponseSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Employees'],
        operation_summary="Update employee",
        operation_description="Update all fields of a specific employee",
        request_body=EmployeeSerializer,
        responses={200: EmployeeSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Employees'],
        operation_summary="Partial update employee",
        operation_description="Update specific fields of an employee",
        request_body=EmployeeSerializer,
        responses={200: EmployeeSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Employees'],
        operation_summary="Delete employee",
        operation_description="Remove an employee record",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['Employees'],
        operation_summary="Get employee roles",
        operation_description="Get list of all possible employee roles",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING),
                description="List of employee roles"
            )
        }
    )
    @action(detail=False, methods=['get'])
    def get_employee_roles(self, request, pk=None):
        roles = [role.value for role in EmployeeRole]
        return Response(roles)