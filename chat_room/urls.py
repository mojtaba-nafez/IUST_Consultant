from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConnectedUser.as_view(), name='get_connected_users'),
    path('<int:UserID>/', views.MessageHistory.as_view(), name='get_message_history'),
]
