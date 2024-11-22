from rest_framework import serializers

from admin_panel.models import Employee
from admin_panel.serializers.university.organization import OrganizationSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeResponseSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Employee
        fields = "__all__"
