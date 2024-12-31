import uuid
from django.db import models
from utils.timestamp_mixin import TimestampMixin


class ExamEmployeeRole(models.TextChoices):
    EVALUATOR = "EVALUATOR", "Evaluator"
    MODERATOR = "MODERATOR", "Moderator"
    SCANNER = "SCANNER", "Scanner"


class ExamEmployee(TimestampMixin):
    """
    Model to manage employee assignments to exams with different roles
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    exam_batch = models.ForeignKey(
        'ExamBatch',
        on_delete=models.CASCADE,
        related_name='exam_employees'
    )
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='exam_assignments'
    )
    role = models.CharField(
        max_length=50,
        choices=ExamEmployeeRole.choices,
        help_text="Role of the employee for this exam"
    )
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='exam_employees'
    )

    class Meta:
        unique_together = ['exam_batch', 'employee', 'role']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee} - {self.role} - {self.exam_batch}"

