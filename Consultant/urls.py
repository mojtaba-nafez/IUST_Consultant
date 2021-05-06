"""Consultant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from User import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User.user_urls')),
    path('consultant/', include('User.consultant_urls')),
    path('profile/', views.UserProfileAPI.as_view(), name="user profile"),
    path('profile/<str:username>/', views.AnotherUserProfileAPI.as_view(), name="another user profile"),
    path('channel-message/<int:channelId>/', include('message.urls')),
    path('request/', include('request.urls')),
    path('channel/', include('channel.urls')),
    path('calendar/', include('calendar_.urls')),
    path('swagger/', views.SwaggerUI.as_view(), name='swagger-ui')
]

urlpatterns += staticfiles_urlpatterns()