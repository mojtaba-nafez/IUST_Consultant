from django.urls import path
from . import views
from channel.views import UserChannelsAPI, UserRoleInChannelAPI

urlpatterns = [
    path('signup-activate-email/', views.UserSignupAPI.as_view(), name='user_signup_email_auth_api'),
    path('signup/', views.UserSignupAPI.as_view(), name='user_signup_api'),
    path('resent-code/', views.GetNewAuthenticationCode.as_view(), name='resent-activation-email-code'),
    path('login/', views.LoginAPI.as_view(), name='user_login_api'),
    path('logout/', views.LogoutAPI.as_view(), name='user_logout_api'),
    path('channels/', UserChannelsAPI.as_view(), name='user channels'),
    path('channel-role/<int:channelId>/', UserRoleInChannelAPI.as_view(), name='user channels'),
]
