from rest_framework import serializers
from channel.models import *
from User.models import BaseUser
from message.models import ChatMessage


class ChannelMessageCreatorField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

class DirectMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, read_only=True)
    sender= ChannelMessageCreatorField(allow_null=False, allow_empty=False, read_only=True)
    receiver =ChannelMessageCreatorField(allow_null=False, allow_empty=False, read_only=True)
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


class ChatMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, read_only=True)
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
    receiver_username = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True)

    def create(self, validated_data):
        del validated_data['receiver_username']
        return ChatMessage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.message_type = validated_data.get('message_type', instance.message_type)
        instance.message_file = validated_data.get('message_file', instance.message_file)
        instance.save()
        return instance
