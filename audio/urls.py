from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_audio, name='upload'),
    path('result/<int:pk>/', views.audio_result, name='result'),
]
