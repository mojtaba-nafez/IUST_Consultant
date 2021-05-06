from django.contrib import admin
from .models import *


class ConsultantTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date']


admin.site.register(ConsultantTime, ConsultantTimeAdmin)
