from rest_framework import serializers
from admin_panel.exam_employee.model import ExamEmployee, ExamEmployeeRole
from admin_panel.users.serializers.employee import EmployeeResponseSerializer
from admin_panel.exam_batch.serializer import ExamBatchResponseSerializer


from rest_framework import serializers



class ExamEmployeeAssignmentSerializer(serializers.Serializer):
    """
    Serializer for assigning multiple employees to an exam with a specific role
    """
    exam_batch = serializers.UUIDField(
        help_text="UUID of the exam batch to assign employees to"
    )
    employee_ids = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="List of employee IDs to assign"
    )
    role = serializers.ChoiceField(
        choices=ExamEmployeeRole.choices,
        help_text="Role to assign to the employees"
    )


class ExamEmployeeResponseSerializer(serializers.ModelSerializer):
    employee = EmployeeResponseSerializer()
    
    class Meta:
        model = ExamEmployee
        fields = ['id', 'employee', 'role', 'created_at', 'updated_at']


class PaperStatisticsSerializer(serializers.Serializer):
    total = serializers.IntegerField(
        help_text="Total number of papers assigned"
    )
    evaluated = serializers.IntegerField(
        help_text="Number of papers marked as FINISHED"
    )
    in_progress = serializers.IntegerField(
        help_text="Number of papers marked as IN_PROGRESS"
    )
    not_started = serializers.IntegerField(
        help_text="Number of papers marked as NOT_STARTED"
    )


class EmployeeBatchStatisticsSerializer(serializers.Serializer):
    """
    Serializer for exam batch details with paper statistics
    """
    exam_batch = ExamBatchResponseSerializer(
        help_text="Complete exam batch details"
    )
    paper_statistics = PaperStatisticsSerializer(
        help_text="Statistics about paper evaluation status"
    )
    role = serializers.CharField(
        help_text="Role of the employee in this exam batch"
    )