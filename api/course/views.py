from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . import serializers
from .models import Course
from .. import permissions


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated, permissions.ReadOnly | permissions.IsOwner]
