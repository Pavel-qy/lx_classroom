from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    lectures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teacher = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    student = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    hometasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    homeworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'teacher', 'student', 'courses',
                  'lectures', 'hometasks', 'homeworks', 'comments']
