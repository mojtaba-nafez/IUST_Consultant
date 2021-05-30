from rest_framework import serializers
from channel.models import *
from User.models import BaseUser


class ConsultantField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username": value.username,
            "phone_number": value.phone_number,
            "first_name": value.first_name,
            "last_name": value.last_name
        }


class SubscriberListField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username": value.username,
            "email": value.email
        }


class ChannelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False, )
    consultant = ConsultantField(read_only=True, allow_null=False, allow_empty=False, )
    name = serializers.CharField(allow_null=False, allow_blank=False, required=True, max_length=50)
    description = serializers.CharField(allow_blank=True, allow_null=True, max_length=500, required=True)
    invite_link = serializers.CharField(allow_null=False, allow_blank=False, max_length=32, required=True)
    avatar = serializers.FileField(required=False, allow_null=True, allow_empty_file=True)

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)


class EditChannelSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=False, allow_blank=False, required=False, max_length=50)
    description = serializers.CharField(allow_blank=True, allow_null=True, max_length=500, required=False)
    invite_link = serializers.CharField(allow_null=False, allow_blank=False, max_length=32, required=False)
    avatar = serializers.FileField(allow_empty_file=True, allow_null=True, required=False)


class ChannelSubscriptionSerializer(serializers.Serializer):
    invite_link = serializers.CharField(allow_null=False, allow_blank=False, max_length=32, required=True)


class DeleteSubscriberSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_null=False, allow_blank=False, required=True)
