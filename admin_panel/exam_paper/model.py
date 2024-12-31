import uuid
from django.db import models
from admin_panel.exams.model import Exam
from admin_panel.organizations.model import Organization
from admin_panel.students.models.student import Student
from admin_panel.users.models.employee import Employee
from utils.timestamp_mixin import TimestampMixin


class ExamEmployeeRole(models.TextChoices):
    EVALUATOR = "EVALUATOR", "Evaluator"
    MODERATOR = "MODERATOR", "Moderator"
    SCANNER = "SCANNER", "Scanner"


class ExamStudentEvaluatorMappingStatus(models.TextChoices):
    FINISHED = "FINISHED", "Finished"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    NOT_STARTED = "NOT_STARTED", "Not Started"


class ExamPaper(TimestampMixin):
    """
    Model to manage employee assignments to exams with different roles
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='exam_employees'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='exam_student_evaluator_mappings'
    ) 
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='exam_student_evaluator_mappings'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='exam_student_evaluator_mappings'
    )
    status = models.CharField(
        max_length=50,
        choices=ExamStudentEvaluatorMappingStatus.choices,
        help_text="Status of the exam paper"
    )

    class Meta:
        unique_together = ['exam', 'employee', 'student']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.employee.first_name} - {self.student.first_name} - {self.exam.name}"

