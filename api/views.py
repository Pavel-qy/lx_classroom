from django.contrib.auth.models import User
from rest_framework import generics, decorators, response, reverse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . import serializers
from . import permissions
from . import filters
from .models import Course, Lecture, Hometask, Homework, Comment


@decorators.api_view(['GET'])
def api_root(request):
    return response.Response({
        'users': reverse.reverse('users', request=request),
        'courses': reverse.reverse('courses', request=request),
        'lectures': reverse.reverse('lectures', request=request),
        'hometasks': reverse.reverse('hometasks', request=request),
        'homeworks': reverse.reverse('homeworks', request=request),
        'comments': reverse.reverse('comments', request=request),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # filter_backends = [IsCourseMemberFilterBackend]  # doesn't work with anonymous users

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated, permissions.ReadOnly | permissions.IsOwner]


class LectureList(generics.ListCreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = serializers.LectureSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByTeacherOnly]
    filter_backends = [filters.IsCourseMemberFilterBackend]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LectureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = serializers.LectureSerializer
    permission_classes = [IsAuthenticated, permissions.IsTeacher | permissions.StudentReadOnly]


class HometaskList(generics.ListCreateAPIView):
    queryset = Hometask.objects.all()
    serializer_class = serializers.HometaskSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByTeacherOnly]
    filter_backends = [filters.IsCourseMemberFilterBackend]

    def perform_create(self, serializer):
        lecture_id = int(self.request.data['lecture'])
        course = Lecture.objects.get(id=lecture_id).course
        serializer.save(owner=self.request.user, course=course)


class HometaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hometask.objects.all()
    serializer_class = serializers.HometaskSerializer
    permission_classes = [IsAuthenticated, permissions.IsTeacher | permissions.StudentReadOnly]


class HomeworkList(generics.ListCreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = serializers.HomeworkStudentSerializer
    permission_classes = [IsAuthenticated, permissions.POSTByStudentOnly]
    filter_backends = [filters.IsOwnerOrTeacherFilterBackend]

    def perform_create(self, serializer):
        hometask_id = int(self.request.data['hometask'])
        lecture = Hometask.objects.get(id=hometask_id).lecture
        serializer.save(owner=self.request.user, course=lecture.course, lecture=lecture)


class HomeworkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Homework.objects.all()
    permission_classes = [IsAuthenticated, permissions.IsOwner | permissions.IsTeacher]

    def get_serializer_class(self):
        # print('\n', f'{dir(self.request)=}', '\n')
        # print('\n', f'{self.request.user.homeworks.values_list("id", flat=True)=}', '\n')
        # print('\n', f'{self.request.parser_context["kwargs"]["pk"]=}', '\n')
        # print('\n', f'{self.request.__dict__=}', '\n')
        if (
            self.request.parser_context['kwargs']['pk'] in
            self.request.user.homeworks.values_list('id', flat=True)
        ):
            return serializers.HomeworkStudentSerializer
        else:
            return serializers.HomeworkTeacherSerializer


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
