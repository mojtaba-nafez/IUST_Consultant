from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ConsultantSignupAPI.as_view(), name='consultant_signup_api'),
    path('login/', views.LoginAPI.as_view(), name='consultant_login_api'),
    path('logout/', views.LogoutAPI.as_view(), name='consultant_logout_api'),
]