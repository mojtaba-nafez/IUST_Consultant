from rest_framework import serializers
from channel.models import *
from django.core.validators import MaxValueValidator, MinValueValidator


class ReserveConsultantTimeSerializer(serializers.Serializer): 
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    title = models.CharField( max_length=200, null=False, blank=False)
    description = models.CharField( max_length=50, null=True, blank=True)
    consultant_id = serializers.IntegerField(read_only=True, allow_null=False, )
