from rest_framework import permissions
from .homework.models import Homework
from .lecture.models import Lecture


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course_id = obj.course_id
        return course_id in request.user.teacher.values_list('id', flat=True)


class StudentReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.course_id in request.user.student.values_list('id', flat=True)


class POSTByTeacherOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or not request.data:
            return True
        if 'course' in request.data:
            course_id = int(request.data['course'])
        elif 'lecture' in request.data:
            lecture_id = int(request.data['lecture'])
            course_id = Lecture.objects.get(id=lecture_id).course_id
        elif 'homework' in request.data:
            homework_id = int(request.data['homework'])
            course_id = Homework.objects.get(id=homework_id).course_id
        else:
            course_id = None
        return course_id in request.user.teacher.values_list('id', flat=True)


class POSTByStudentOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or not request.data:
            return True
        hometask_id = int(request.data['hometask'])
        course_id = Lecture.objects.get(id=hometask_id).course_id
        user_courses_student = request.user.student.values_list('id', flat=True)
        return course_id in user_courses_student


class POSTByOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or not request.data:
            return True
        homework_id = int(request.data['homework'])
        return homework_id in request.user.homeworks.values_list('id', flat=True)
