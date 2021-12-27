from django.db.models import Q
from rest_framework import filters


class IsCourseMemberFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # print(f'{request=}', f'{getattr(queryset[0], "lecture_id", False)=}', f'{view.__class__.__name__=}', sep='\n')
        courses_user_teacher = request.user.teacher.values_list('id', flat=True)
        courses_user_student = request.user.student.values_list('id', flat=True)
        # if view.__class__.__name__ == 'CourseList':
        #     return queryset.filter(Q(id__in=courses_user_teacher) | Q(id__in=courses_user_student))
        # elif view.__class__.__name__ == 'LectureList':
        #     return queryset.filter(Q(course_id__in=courses_user_teacher) | Q(course_id__in=courses_user_student))
        # elif view.__class__.__name__ == 'HometaskList':
        #     return queryset.filter(
        #         Q(lecture_id__course_id__in=courses_user_teacher) | Q(lecture_id__course_id__in=courses_user_student)
        #     )
        # return queryset
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
