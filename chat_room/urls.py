from django.urls import path
from . import views

urlpatterns = [
    path('direct/', views.ConnectedUser.as_view(), name='get_connected_users'),
    path('direct/<int:UserID>/', views.MessageHistory.as_view(), name='get_message_history'),
    path('file/', views.MessageHistory.as_view(), name='get_message_history'),
]
