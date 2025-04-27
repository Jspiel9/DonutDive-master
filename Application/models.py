# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    last_reward_claim_time = models.DateTimeField(null=True, blank=True)