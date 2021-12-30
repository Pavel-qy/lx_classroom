from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Homework
from .. import permissions, filters
from ..hometask.models import Hometask


class HomeworkList(generics.ListCreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = serializers.HomeworkStudentSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByStudentOnly]
    filter_backends = [filters.IsOwnerOrTeacherFilterBackend]

    def perform_create(self, serializer):
        hometask_id = int(self.request.data['hometask'])
        lecture = Hometask.objects.get(id=hometask_id).lecture
        serializer.save(owner=self.request.user, course=lecture.course, lecture=lecture)


class HomeworkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Homework.objects.all()
    permission_classes = [IsAuthenticated, permissions.IsOwner | permissions.IsTeacher]

    def get_serializer_class(self):
        if (
                self.request.parser_context['kwargs'].get('pk') in
                self.request.user.homeworks.values_list('id', flat=True)
        ):
            return serializers.HomeworkStudentSerializer
        else:
            return serializers.HomeworkTeacherSerializer
