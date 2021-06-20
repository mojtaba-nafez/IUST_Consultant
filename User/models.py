from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.utils import timezone


def validate_phone_number(phone_number):
    from django.core.exceptions import ValidationError
    # check phone number regex and return ValidationError
    import re
    if len(phone_number) != 11 or re.search(r"09[0-9]{9}", phone_number) is None:
        raise serializers.ValidationError("Format of phone_number is not true")
    return phone_number


def validate_avatar_extension(value):
    import os
    from django.core.exceptions import ValidationError
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if extension.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension')


class BaseUser(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=11, null=False, blank=False, unique=True,
                                    validators=[validate_phone_number])
    avatar = models.FileField(upload_to="files/user_avatar", null=True, blank=True,
                              validators=[validate_avatar_extension])
    user_type_choices = [
        ('normal_user', 'normal_user'),
        ('Lawyer', 'Lawyer'),
        ('medical', 'medical'),
        ('EntranceExam', 'EntranceExam'),
        ('Psychology', 'Psychology'),
        ('Immigration', 'Immigration'),
        ('AcademicAdvice', 'AcademicAdvice')
    ]
    user_type = models.CharField(null=False, blank=False, choices=user_type_choices, default="normal_user",
                                 max_length=32)


class UserProfile(BaseUser):
    private_profile = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'UserProfile'


class ConsultantProfile(BaseUser):
    private_profile = models.BooleanField(default=False, null=False, blank=False)
    accepted = models.BooleanField(default=False, null=False, blank=False)
    my_secretaries = models.ManyToManyField(
        UserProfile,
    )
    certificate = models.FileField(upload_to="files/lawyers/certificate", null=True, blank=True)
    count_of_all_comments = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    satisfaction_percentage = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name_plural = 'ConsultantProfile'


class TemporalAuthenticationCode(models.Model):
    code = models.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]{5}$')])
    email = models.EmailField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
