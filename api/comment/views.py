from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Comment
from .. import permissions, filters
from ..homework.models import Homework


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByOwnerOnly | permissions.POSTByTeacherOnly]
    filter_backends = [filters.IsHomeworkOwnerOrTeacherFilterBackend]

    def perform_create(self, serializer):
        homework_id = int(self.request.data['homework'])
        hometask = Homework.objects.get(id=homework_id).hometask
        serializer.save(
            owner=self.request.user, course=hometask.lecture.course,
            lecture=hometask.lecture, hometask=hometask
        )


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]
