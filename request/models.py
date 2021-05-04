from django.db import models
from django.utils import timezone

from User.models import BaseUser, ConsultantProfile
from channel.models import Channel


class Request(models.Model):
    target_user = models.ForeignKey(BaseUser, verbose_name="Target User", on_delete=models.CASCADE)
    request_text = models.CharField(null=True, blank=True, max_length=2000)
    answer_text = models.CharField(null=True, blank=True, max_length=2000)
    request_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    answer_date = models.DateTimeField(null=True, blank=False)
    accept = models.BooleanField(default=False, null=False, blank=False)
    request_type_choices = [
        ("secretary", "secretary"),
        ("join_channel", "join_channel")
    ]
    request_type = models.CharField(default="join_channel", null=False, blank=False, choices=request_type_choices, max_length=64)
    class Meta:
        abstract = True


class SecretaryRequest(Request):
    channel = models.ForeignKey(Channel, verbose_name="Channel", on_delete=models.CASCADE,)


class JoinChannelRequest(Request):
    channel = models.ForeignKey(Channel, verbose_name="Channel", on_delete=models.CASCADE,)
