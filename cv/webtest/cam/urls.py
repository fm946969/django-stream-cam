from django.urls import path, include
from .views import video_feed, index


urlpatterns = [
    path('', index, name='index'),
    path('video_feed/', video_feed, name='video_feed'),
]