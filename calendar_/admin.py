from django.contrib import admin
from .models import *


class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'invite_link']


admin.site.register(Channel, ChannelAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['channel', 'user', 'date_joined']


admin.site.register(Subscription, SubscriptionAdmin)