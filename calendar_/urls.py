from django.urls import path

from video_chat.views import ChatVideoAPI
from . import views


urlpatterns = [
    path('consultant-time/', views.ConsultantTimeAPI.as_view(), name='cr_consultant_time'),
    path('consultant-time/<int:ConsultantTimeId>/', views.ConsultantTimeAPI.as_view(), name='ud_consultant_time'),
    path('consultant-time/video-chat/<int:ConsultantTimeId>/', ChatVideoAPI.as_view(), name='start video chat'),
    path('consultant-time/cancel/<int:ConsultantTimeId>/', views.CancelConsultantTime.as_view(), name='cancel_consultant_time'),
    path('consultant-time/comment/<int:ConsultantTimeId>/', views.CommentAndGradeAPI.as_view(), name='create comment'),
    path('reserve/<int:ConsultantID>/', views.Reserve.as_view(), name='consultant_time'),
]

