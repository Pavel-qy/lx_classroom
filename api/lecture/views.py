from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Lecture
from .. import permissions, filters


class LectureList(generics.ListCreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = serializers.LectureSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByTeacherOnly]
    filter_backends = [filters.IsCourseMemberFilterBackend]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LectureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = serializers.LectureSerializer
    permission_classes = [IsAuthenticated, permissions.IsTeacher | permissions.StudentReadOnly]
