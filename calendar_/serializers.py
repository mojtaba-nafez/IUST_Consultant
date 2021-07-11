from rest_framework import serializers
from .models import *
from django.utils import timezone


class ConsultantTimeReservatore(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "username": value.username,
            "first_name": value.first_name,
            "last_name": value.last_name,
            "phone_number": value.phone_number,
            "avatar": value.avatar.url if value.avatar else None
        }


class ConsultantTimeConsultant(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "username": value.username,
            "phone_number": value.phone_number,
            "avatar": value.avatar.url if value.avatar else None
        }


class ConsultantTimeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    consultant_id = serializers.IntegerField(required=False, allow_null=False, write_only=True)
    start_date = serializers.DateTimeField(required=True, allow_null=False, )
    end_date = serializers.DateTimeField(required=True, allow_null=False, )
    title = serializers.CharField(read_only=True, allow_null=True, allow_blank=True)
    description = serializers.CharField(read_only=True, allow_null=True, allow_blank=True)
    user = ConsultantTimeReservatore(allow_null=True, read_only=True, allow_empty=False)
    consultant = ConsultantTimeConsultant(allow_null=True, allow_empty=True, read_only=True)

    def create(self, validated_data):
        return ConsultantTime.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance

    def validate_start_date(self, start_date):
        if start_date < timezone.now():
            raise serializers.ValidationError("زمان شروع، از زمان حال قدیمی تر است")
        else:
            return start_date

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("زمان پایان از زمان شروع قدیمی تر است")
        return data


class ReserveConsultantTimeSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    title = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=200,
                                  error_messages={
                                      "required": "عنوان برای زمان لازم است",
                                      "null": "عنوان نمیتواند null باشد",
                                      "length": "عنوان حداکثر 200 کاراکتر است",
                                      "blank": "عنوان نمیتواند خالی باشد"
                                  }, )
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False, max_length=500,
                                        error_messages={
                                            "length": "توضیحات حداکثر 500 کاراکتر میتواند باشد",
                                        }, )
    id = serializers.IntegerField(read_only=True, allow_null=False)


class ReservatorField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "username": value.username,
            "first_name": value.first_name,
            "last_name": value.last_name,
            "avatar": value.avatar.url if value.avatar else None,
        }


class CommentAndRateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    user_grade_date = serializers.DateTimeField(read_only=True, allow_null=False)
    user = ReservatorField(read_only=True, allow_null=True, allow_empty=True)
    user_grade = serializers.IntegerField(required=True, allow_null=False, max_value=5, min_value=0)
    user_comment = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=500,
                                         error_messages={'length': "طول متن حداکثر 500 کاراکتر میتواند باشد"})
