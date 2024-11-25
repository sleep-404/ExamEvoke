import uuid
from django.db import models

from admin_panel.models.exams.exam import Exam
from admin_panel.models.exams.exam_batch import ExamBatch
from admin_panel.models.questions.question import Question
from admin_panel.models.university.organization import Organization
from admin_panel.students.models.student import Student
# from admin_panel.models.user.student import Student


class ExamBatchMapping(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    exam = models.ForeignKey(
        Exam,
        related_name="exambatchesexams",
        on_delete=models.CASCADE,
    )
    exambatch = models.ForeignKey(
        ExamBatch,
        related_name="exambatchesbatches",
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )


class ExamQuestionMapping(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    exam = models.ForeignKey(
        Exam,
        related_name="examquestionsexams",
        on_delete=models.CASCADE,
    )
    exambatch = models.ForeignKey(
        Question,
        related_name="examquestionsexambatch",
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )


class ExamBatchStudentMapping(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    student = models.ForeignKey(
        Student,
        related_name="exambatchstudents",
        on_delete=models.CASCADE,
    )
    exambatch = models.ForeignKey(
        ExamBatch,
        related_name="exambatchbatches",
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )
