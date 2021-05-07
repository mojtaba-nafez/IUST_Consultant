from django.urls import path
from . import views

urlpatterns = [
    path('reserve/<int:ConsultantID>/', views.Reserve.as_view(), name='consultant_time'),
]
