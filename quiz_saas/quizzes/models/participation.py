from typing import Union
from django.db import models
from django.contrib.auth.models import User
from . import Quiz
from . import Answer

COMPLETED = "COMPLETED"
NOT_STARTED = "NOT_STARTED"
IN_PROGRESS = "IN_PROGRESS"


class Participation(models.Model):
    user = models.ForeignKey(
        User, related_name="participations", on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz, related_name="participations", on_delete=models.CASCADE
    )
    answers = models.ManyToManyField(Answer, related_name="participations")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @classmethod
    def get_participation_by_id(cls, participation_id) -> "Participation":
        return cls.objects.get(pk=participation_id)

    @property
    def progress(self) -> str:
        number_answers = self.answers.count()
        number_questions = self.quiz.total_questions
        if number_answers == number_questions:
            return COMPLETED
        elif number_answers == 0:
            return NOT_STARTED
        else:
            return f"{IN_PROGRESS}{number_answers}/{number_questions}"

    @property
    def score(self) -> Union[float, None]:
        if self.is_completed == False:
            return None
        total_answers = self.answers.count()
        correct_answers = self.answers.filter(is_correct=True).count()
        return correct_answers / total_answers * 100

    @property
    def is_completed(self) -> bool:
        return self.progress == COMPLETED
