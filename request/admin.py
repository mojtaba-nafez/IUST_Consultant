from django.contrib import admin
from .models import *

class RequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'target_user', 'request_date', 'answer_date',]


admin.site.register(SecretaryRequest, RequestAdmin)
admin.site.register(JoinChannelRequest, RequestAdmin)
