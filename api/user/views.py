from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from . import serializers
from .. import permissions


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUser | permissions.IsUser]
