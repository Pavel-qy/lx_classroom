from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('', views.api_root),
    path('api-auth/', include('rest_framework.urls')),
    path('users/', views.UserList.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('courses/', views.CourseList.as_view(), name='courses'),
    path('courses/<int:pk>', views.CourseDetail.as_view()),
    path('lectures/', views.LectureList.as_view(), name='lectures'),
    path('lectures/<int:pk>', views.LectureDetail.as_view()),
    path('hometasks/', views.HometaskList.as_view(), name='hometasks'),
    path('hometasks/<int:pk>', views.HometaskDetail.as_view()),
    path('homeworks/', views.HomeworkList.as_view(), name='homeworks'),
    path('homeworks/<int:pk>', views.HomeworkDetail.as_view()),
    path('comments/', views.CommentList.as_view(), name='comments'),
    path('comments/<int:pk>', views.CommentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
