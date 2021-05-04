import uuid

from django.db import models
from User.models import ConsultantProfile, BaseUser
from django.utils import timezone

def validate_avatar_extension(value):
    import os
    from django.core.exceptions import ValidationError
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', '.jpeg', '.gif']
    if extension.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension')

class Channel(models.Model):
    subscribers = models.ManyToManyField(BaseUser, verbose_name="", through='channel.Subscription')
    consultant = models.OneToOneField(ConsultantProfile, verbose_name="channel owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    invite_link = models.CharField(null=False, blank=False, max_length=32, unique=True)
    avatar = models.FileField(upload_to="files/channel_avatar/", null=True, blank=True,
                              validators=[validate_avatar_extension])
    class Meta:
        verbose_name_plural = 'Channel'


class Subscription(models.Model):
    channel = models.ForeignKey(Channel, verbose_name="", on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, verbose_name="", on_delete=models.DO_NOTHING)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('channel', 'user',)
        verbose_name_plural = 'Subscription'
