from django.urls import path
from . import views


urlpatterns = [
    path('consultant-time/', views.ConsultantTimeAPI.as_view(), name='cr_consultant_time'),
    path('consultant-time/<int:ConsultantTimeId>/', views.ConsultantTimeAPI.as_view(), name='ud_consultant_time'),
]