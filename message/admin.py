from django.contrib import admin

from message.models import ChannelMessage, ChatMessage


class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'text', 'message_type']


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'text', 'message_type', 'sender', 'receiver']


admin.site.register(ChannelMessage, ChannelMessageAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
