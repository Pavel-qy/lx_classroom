from . import views
from django.urls import path


urlpatterns = [
    path('', views.CommentList.as_view(), name='comments'),
    path('<int:pk>/', views.CommentDetail.as_view()),
    ]
