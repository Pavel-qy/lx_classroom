from rest_framework import permissions
from .models import Lecture, Homework


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # course_id = obj.hometask.lecture.course_id
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


# class IsTeacherOrStudentReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # print(f'{self=}', f'{request=}', f'{view=}', f'{obj=}', sep='\n')
#         # print(f'{obj.__dict__=}')
#         if getattr(obj, 'course_id', False):
#             course_id = obj.course_id
#         elif getattr(obj, 'lecture_id', False):
#             course_id = obj.lecture.course_id
#         else:
#             course_id = None
#         if request.method in permissions.SAFE_METHODS:
#             for course in request.user.student.all():
#                 if course.id == course_id:
#                     return True
#         for course in request.user.teacher.all():
#             if course.id == course_id:
#                 return True
