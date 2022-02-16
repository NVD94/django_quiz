from django.db import models
from django.contrib.auth.models import User
import random

from . import Quiz


class Question(models.Model):
    content = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
