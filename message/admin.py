from django.contrib import admin

from message.models import ChannelMessage, DirectMessage


class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'text', 'message_type']

class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'text', 'message_type', 'sender', 'reciever']

admin.site.register(ChannelMessage, ChannelMessageAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)