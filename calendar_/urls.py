from django.urls import path

from . import views

urlpatterns = [
    path('consultant-time/', views.ConsultantTimeAPI.as_view(), name='cr_consultant_time'),
    path('consultant-time/<int:ConsultantTimeId>/', views.ConsultantTimeAPI.as_view(), name='ud_consultant_time'),
    path('consultant-time/cancel/<int:ConsultantTimeId>/', views.CancelConsultantTime.as_view(),
         name='cancel_consultant_time'),
    path('consultant-time/comment/<int:ConsultantTimeId>/', views.CommentAndGradeAPI.as_view(), name='create comment'),
    path('reserve/<int:ConsultantID>/', views.Reserve.as_view(), name='consultant_time'),
]
