from django.db.models import Q
from rest_framework import filters


class IsCourseMemberFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        courses_user_teacher = request.user.teacher.values_list('id', flat=True)
        courses_user_student = request.user.student.values_list('id', flat=True)
        return queryset.filter(Q(course_id__in=courses_user_teacher) | Q(course_id__in=courses_user_student))


class IsOwnerOrTeacherFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        courses_user_teacher = request.user.teacher.values_list('id', flat=True)
        return queryset.filter(
            Q(owner_id=request.user.id) | Q(course_id__in=courses_user_teacher)
        )


class IsHomeworkOwnerOrTeacherFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        courses_user_teacher = request.user.teacher.values_list('id', flat=True)
        return queryset.filter(
            Q(homework__owner_id=request.user.id) | Q(course_id__in=courses_user_teacher)
        )
