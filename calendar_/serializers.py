from rest_framework import serializers
from .models import *
from django.utils import timezone


class ConsultantTimeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    consultant_id = serializers.IntegerField(required=False, allow_null=False, write_only=True)
    start_date = serializers.DateTimeField(required=True, allow_null=False,)
    end_date = serializers.DateTimeField(required=True, allow_null=False, )
    title = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=200,
                                  error_messages={
                                      "required": "عنوان برای زمان لازم است",
                                      "null": "عنوان نمیتواند null باشد",
                                      "length": "عنوان حداکثر 200 کاراکتر است",
                                      "blank": "عنوان نمیتواند خالی باشد"
                                  },)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=500)

    def create(self, validated_data):
        return ConsultantTime.objects.create(**validated_data)

    def validate_start_date(self, start_date):
        if start_date < timezone.now():
            raise serializers.ValidationError("زمان شروع، از زمان حال قدیمی تر است")
        else:
            return start_date

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("زمان پایان از زمان شروع قدیمی تر است")
        return data
