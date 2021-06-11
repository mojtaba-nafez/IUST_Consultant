from rest_framework import serializers
from .models import *


class VideoChatRequestSerializer(serializers.Serializer):
    meetingId = serializers.IntegerField(read_only=True, allow_null=False)
