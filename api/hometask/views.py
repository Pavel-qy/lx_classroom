from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Hometask
from .. import permissions, filters
from ..lecture.models import Lecture


class HometaskList(generics.ListCreateAPIView):
    queryset = Hometask.objects.all()
    serializer_class = serializers.HometaskSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByTeacherOnly]
    filter_backends = [filters.IsCourseMemberFilterBackend]

    def perform_create(self, serializer):
        lecture_id = int(self.request.data['lecture'])
        course = Lecture.objects.get(id=lecture_id).course
        serializer.save(owner=self.request.user, course=course)


class HometaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hometask.objects.all()
    serializer_class = serializers.HometaskSerializer
    permission_classes = [IsAuthenticated, permissions.IsTeacher | permissions.StudentReadOnly]