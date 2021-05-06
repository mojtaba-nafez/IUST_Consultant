from django.urls import path
from . import views


urlpatterns = [
    path('consultant-time/', views.ConsultantTime.as_view(), name='crud_consultant_time'),
]