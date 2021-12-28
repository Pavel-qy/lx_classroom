from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
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

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
