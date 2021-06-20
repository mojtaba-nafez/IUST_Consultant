from django.urls import path
from . import views
from calendar_.views import CommentAndGradeAPI

urlpatterns = [
    path('signup/', views.ConsultantSignupAPI.as_view(), name='consultant_signup_api'),
    path('signup-activate-email/', views.ConsultantSignupAPI.as_view(), name='consultant_signup_email_auth_api'),
    path('resent-code/', views.GetNewAuthenticationCode.as_view(), name='resent-activation-email-code'),
    path('login/', views.LoginAPI.as_view(), name='consultant_login_api'),
    path('logout/', views.LogoutAPI.as_view(), name='consultant_logout_api'),
    path('search-consultants/', views.SearchConsultantsAPI.as_view(), name='search_consultants'),
    path('comment/<str:ConsultantUsername>/', CommentAndGradeAPI.as_view(), name='get consultant comments'),
]