from django.contrib import admin

from message.models import ChannelMessage


class ChannelMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'text', 'message_type']


admin.site.register(ChannelMessage, ChannelMessageAdmin)
