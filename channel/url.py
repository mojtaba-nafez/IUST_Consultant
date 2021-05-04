from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChannelAPI.as_view(), name='channel_crud'),
    path('<int:channelId>/', views.ChannelAPI.as_view(), name='channel_crud'),
    path('invite-link/', views.CreateLinkAPI.as_view(), name='create_random_invite_link'),
    path('subscription/', views.ChannelSubscriptionAPI.as_view(), name='subscription'),
    path('search-for-channel/', views.SearchChannel.as_view(), name='Search_for_channels'),
    path('suggestion-channel/', views.SuggestionChannel.as_view(), name='suggestion_channels'),
    path('channel-subscriber/<int:channelId>/', views.ChannelSubscribers.as_view(), name='channel_subscriber'),
    path('channel-admins/<int:channelId>/', views.ChannelAdmins.as_view(), name='channel_admins'),
    path('update-channel-inf/<int:channelId>/', views.EditChannel.as_view(), name='update_channel_inf'),

]
