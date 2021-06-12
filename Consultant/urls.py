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
from User import views as user_view
from Consultant import views as consultant_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from chat_room import views as chat_views
from video_chat.views import ChatVideoAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('User.user_urls')),
    path('consultant/', include('User.consultant_urls')),
    path('profile/', user_view.UserProfileAPI.as_view(), name="user profile"),
    path('profile/<str:username>/', user_view.AnotherUserProfileAPI.as_view(), name="another user profile"),
    path('channel-message/<int:channelId>/', include('message.urls')),
    path('request/', include('request.urls')),
    path('channel/', include('channel.urls')),
    path('calendar/', include('calendar_.urls')),
    path('swagger/', user_view.SwaggerUI.as_view(), name='swagger-ui'),
    path('swagger/', user_view.SwaggerUI.as_view(), name='swagger-ui'),
    path('calendar/', include('calendar_.urls')),
    path('video-chat/', include('video_chat.urls')),
    path('fakeData/', consultant_view.InsertFakeData.as_view(), name='insert-fake-data'),
    path('chat/', include('chat_room.urls'), name='chat_room'),
    #path('chat/', chat_views.index, name='index'),
    #path('chat/<str:room_name>/', chat_views.room, name='index'),
    #path('test/', ChatVideoAPI.as_view(), name='index'),
]

urlpatterns += staticfiles_urlpatterns()
