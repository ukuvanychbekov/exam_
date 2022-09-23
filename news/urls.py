from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('news/', views.NewsListCreateAPIview.as_view()),
    path('news/<int:pk>/', views.NewsRetrieveUpdateDestroyAPIView.as_view()),
    path('news/<int:news_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('news/<int:news_id>/<str:status_slug>/', views.PostNewsLike.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/<str:status_slug>/', views.PostCommentLike.as_view()),
    path('statuses/', views.StatusViewSet.as_view()),
    path('statuses/<int:pk>/', views.StatusRetrieveUpdateDestroyAPIView.as_view()),

]