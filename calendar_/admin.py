from django.contrib import admin
from .models import *

class ConsultantTimeAdmin(admin.ModelAdmin):
    list_display = ['consultant', 'user', 'start_date', 'end_date', 'title']


admin.site.register(ConsultantTime, ConsultantTimeAdmin)
