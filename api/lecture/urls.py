from . import views
from django.urls import path


urlpatterns = [
    path('', views.LectureList.as_view(), name='lectures'),
    path('<int:pk>/', views.LectureDetail.as_view()),
    ]
