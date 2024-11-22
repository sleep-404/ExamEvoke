from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from admin_panel.models import ExamBatch
from admin_panel.serializers.exams.exam_batch import (
    ExamBatchSerializer,
    ExamBatchResponseSerializer
) 


class ExamBatchViewset(viewsets.ModelViewSet):
    queryset = ExamBatch.objects.all()
    serializer_class = ExamBatchSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['exam', 'mode', 'name']
    search_fields = ['name', 'details']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExamBatchResponseSerializer
        return ExamBatchSerializer
