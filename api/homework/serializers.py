from rest_framework import serializers
from .models import Homework


class HomeworkStudentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.id')
    lecture = serializers.ReadOnlyField(source='lecture.id')
    grade = serializers.ReadOnlyField(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'created', 'owner', 'course', 'lecture', 'hometask', 'url', 'grade', 'comments']


class HomeworkTeacherSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.id')
    lecture = serializers.ReadOnlyField(source='lecture.id')
    hometask = serializers.PrimaryKeyRelatedField(read_only=True)
    url = serializers.ReadOnlyField(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'created', 'owner', 'course', 'lecture', 'hometask', 'url', 'grade', 'comments']
