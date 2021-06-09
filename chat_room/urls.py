from django.urls import path
from . import views

urlpatterns = [
    path('direct/contact/', views.ConnectedUser.as_view(), name='get_connected_users'),
    path('direct/history/<str:UserName>/', views.MessageHistory.as_view(), name='get_message_history'),
    path('direct/message/', views.ChatMessageAPI.as_view(), name='create chat message'),
    path('direct/message/<int:ChatMessageId>/', views.ChatMessageAPI.as_view(), name='Get and Put chat message'),
]
