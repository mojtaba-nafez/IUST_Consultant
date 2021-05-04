from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChannelMessageAPI.as_view(), name='message_crud'),
    path('<int:messageId>/', views.ChannelMessageAPI.as_view(), name='get messages'),
]