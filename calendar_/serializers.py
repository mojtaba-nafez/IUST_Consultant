from rest_framework import serializers
from .models import *



class ConsultantTimeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    consultant_id = serializers.IntegerField(required=False, allow_null=False, write_only=True)
    start_date = serializers.DateTimeField(required=True, allow_null=False,)
    end_date = serializers.DateTimeField(required=True, allow_null=False,)
    title = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=200)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=500)

    def create(self, validated_data):
        return ConsultantTime.objects.create(**validated_data)