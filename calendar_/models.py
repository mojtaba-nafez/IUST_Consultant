from django.db import models
from User.models import ConsultantProfile, UserProfile, BaseUser
from django.core.validators import MaxValueValidator, MinValueValidator


class ConsultantTime(models.Model):
    consultant = models.ForeignKey(ConsultantProfile, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")

    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    cost = models.FloatField(default=0)
    user_grade = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], null=True, blank=True)
    user_grade_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    user_comment = models.TextField(max_length=500, null=True, blank=True)

    whereby_meeting_id = models.IntegerField(null=True, blank=True, )
    whereby_room_url = models.CharField(null=True, blank=True, max_length=500)
    whereby_host_room_url = models.CharField(null=True, blank=True, max_length=500)
