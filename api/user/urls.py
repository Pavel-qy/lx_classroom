from . import views
from django.urls import path


urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    path('<int:pk>/', views.UserDetail.as_view()),
    ]
