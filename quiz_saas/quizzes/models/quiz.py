from typing import List
from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    user = models.ForeignKey(User, related_name="quizzes", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def total_questions(self) -> int:
        return self.questions.count()

    @property
    def participation_list(self):
        return self.participations.all()

    @classmethod
    def get_quiz_by_id(cls, quiz_id: int):
        return cls.objects.filter(id=quiz_id).first()
