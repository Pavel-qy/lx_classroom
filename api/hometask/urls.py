from . import views
from django.urls import path


urlpatterns = [
    path('', views.HometaskList.as_view(), name='hometasks'),
    path('<int:pk>/', views.HometaskDetail.as_view()),
    ]
