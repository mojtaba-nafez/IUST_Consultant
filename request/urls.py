from django.urls import path
from . import views

urlpatterns = [
    path('applicant/', views.ApplicantRequestAPI.as_view(), name='crud_secretary_for_consultant'),
    path('responder/', views.ResponderRequestAPI.as_view(),
         name="get all user requests"),
]
