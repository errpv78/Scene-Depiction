from django.urls import path
from myApp import views

app_name = "myApp"

urlpatterns = [
    path('', views.home, name='home'),
    path('live_stream/', views.live_stream, name='live_stream'),
    path('play_recorded_video/', views.play_recorded_video, name='play_recorded_video'),
]