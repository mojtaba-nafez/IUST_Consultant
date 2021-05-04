from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserSignupAPI.as_view(), name='user_signup_api'),
    path('login/', views.LoginAPI.as_view(), name='user_login_api'),
    path('logout/', views.LogoutAPI.as_view(), name='user_logout_api'),
]
