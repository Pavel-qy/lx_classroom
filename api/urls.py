from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.api_root),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('api.auth.urls')),
    path('users/', include('api.user.urls')),
    path('courses/', include('api.course.urls')),
    path('lectures/', include('api.lecture.urls')),
    path('hometasks/', include('api.hometask.urls')),
    path('homeworks/', include('api.homework.urls')),
    path('comments/', include('api.comment.urls')),
]
