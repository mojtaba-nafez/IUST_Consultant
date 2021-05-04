from django.db import models
from User.models import ConsultantProfile, UserProfile
from django.core.validators import MaxValueValidator, MinValueValidator

class ConsultantTime(models.Model):
    consultant = models.ForeignKey( ConsultantProfile, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    title = models.CharField( max_length=200)
    description = models.CharField( max_length=50, null=True, blank=True)
    cost = models.FloatField(default=0)
    user_grade = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], null=True, blank=True)
    user_comment = models.TextField(max_length=500, null=True, blank=True)