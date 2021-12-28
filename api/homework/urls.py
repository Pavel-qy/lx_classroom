from . import views
from django.urls import path


urlpatterns = [
    path('', views.HomeworkList.as_view(), name='homeworks'),
    path('<int:pk>/', views.HomeworkDetail.as_view()),
    ]
