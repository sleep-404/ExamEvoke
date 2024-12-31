from rest_framework import serializers
from admin_panel.exam_paper.model import ExamPaper
from admin_panel.students.serializer import StudentResponseSerializer
from admin_panel.users.serializers.employee import EmployeeResponseSerializer



class ExamPaperResponseSerializer(serializers.ModelSerializer):
    employee = EmployeeResponseSerializer()
    student = StudentResponseSerializer()
    class Meta:
        model = ExamPaper
        fields = "__all__"