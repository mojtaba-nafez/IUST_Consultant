from abc import ABC

from rest_framework import serializers
from .models import *
from django.core.validators import RegexValidator


class LoginSerializer(serializers.Serializer):
    email_username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6, max_length=128,
                                     error_messages={
                                         "length": "طول رمز حداقل ۶ کاراکتر باید باشد",
                                     }, )


class BaseUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)
    avatar = serializers.FileField(allow_empty_file=True, allow_null=True, required=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6, max_length=128,
                                     write_only=True, error_messages={
            "length": "طول رمز حداقل ۶ کاراکتر باید باشد",
        }, )
    private_profile = serializers.BooleanField(default=False, allow_null=False)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

    def validate_phone_number(self, phone_number):
        """
        Check the phone_number regex.
        """
        import re
        if len(phone_number) != 11 or re.search(r"09[0-9]{9}", phone_number) is None:
            raise serializers.ValidationError("فرمت شماره‌تلفن صحیح نیست")
        return phone_number


class UserProfileSerializer(BaseUserSerializer):
    user_type = serializers.CharField(read_only=True, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)


class ConsultantProfileSerializer(BaseUserSerializer):
    certificate = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)
    consultant_types = (
        ('Lawyer', 'Lawyer'),
        ('medical', 'medical'),
        ('EntranceExam', 'EntranceExam'),
        ('Psychology', 'Psychology'),
        ('Immigration', 'Immigration'),
        ('AcademicAdvice', 'AcademicAdvice')
    )
    user_type = serializers.ChoiceField(choices=consultant_types, required=True)

    def create(self, validated_data):
        return ConsultantProfile.objects.create(**validated_data)

    def validate_certificate(self, certificate_file):
        # TODO CHECK CERTIFICATE EXTENSION
        return certificate_file


class SearchConsultantSerializer(BaseUserSerializer):
    consultant_types = (
        ('Lawyer', 'Lawyer'),
        ('medical', 'medical'),
        ('EntranceExam', 'EntranceExam'),
        ('Psychology', 'Psychology'),
        ('Immigration', 'Immigration'),
        ('AcademicAdvice', 'AcademicAdvice')
    )
    user_type = serializers.ChoiceField(choices=consultant_types, required=True)
    count_of_all_comments = serializers.IntegerField(default=0, validators=[MinValueValidator(0)])
    satisfaction_percentage = serializers.IntegerField(default=0,
                                                       validators=[MinValueValidator(0), MaxValueValidator(100)])
