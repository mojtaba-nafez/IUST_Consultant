from rest_framework import serializers
from channel.models import *
from User.models import BaseUser


class DirectMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, read_only=True)
    sender_id = serializers.IntegerField(allow_null=False, read_only=True)
    receiver_id = serializers.IntegerField(allow_null=False, read_only=True)
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
    receiver_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
