from rest_framework import serializers
from message.models import *


class ChannelMessageCreatorField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "username": value.username,
            "phone_number": value.phone_number
        }


class ChannelMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, read_only=True)
    channel_id = serializers.IntegerField(allow_null=False, read_only=True)
    creator = ChannelMessageCreatorField(allow_null=False, allow_empty=False, read_only=True)
    text = serializers.CharField(max_length=2000, required=False, allow_null=False, allow_blank=False,
                                 error_messages={'length': "طول متن حداکثر ۲۰۰ کاراکتر میتواند باشد"})
    message_choice = [
        ('t', 'text'),
        ('i', 'image'),
        ('v', 'video'),
        ('a', 'audio'),
    ]
    message_type = serializers.ChoiceField(choices=message_choice, required=True, allow_null=False,
                                           allow_blank=False)
    message_file = serializers.FileField(required=False, allow_null=False, allow_empty_file=False)

    def create(self, validated_data):
        return ChannelMessage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.message_file = validated_data.get('message_file', instance.message_file)
        instance.save()
        return instance
