from rest_framework import serializers
from channel.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timezone

class ReserveConsultantTimeSerializer(serializers.Serializer): 
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    title = serializers.CharField( max_length=200)
    description = serializers.CharField( max_length=50)