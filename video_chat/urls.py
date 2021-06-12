from django.urls import path

from . import views

urlpatterns = [
    path('consultant-time/start/<int:ConsultantTimeId>/', views.ChatVideoAPI.as_view(), name='start video chat'),
]
