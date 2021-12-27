from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Course, Lecture, Hometask, Homework, Comment


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


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    lectures = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    hometasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    homeworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # teacher = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Course
        fields = [
            'id', 'created', 'owner', 'title', 'teachers', 'students',
            'lectures', 'hometasks', 'homeworks', 'comments'
        ]


class LectureSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    hometasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Lecture
        fields = ['id', 'created', 'owner', 'course', 'title', 'document', 'hometasks']


class HometaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.id')
    homeworks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Hometask
        fields = ['id', 'created', 'owner', 'course', 'lecture', 'title', 'body', 'homeworks']


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


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    course = serializers.ReadOnlyField(source='course.id')
    lecture = serializers.ReadOnlyField(source='lecture.id')
    hometask = serializers.ReadOnlyField(source='hometask.id')

    class Meta:
        model = Comment
        fields = ['id', 'created', 'owner', 'course', 'lecture', 'hometask', 'homework', 'body']
