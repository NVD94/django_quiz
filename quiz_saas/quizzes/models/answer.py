from django.db import models
from . import Question


class Answer(models.Model):
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )

    @classmethod
    def get_answer_by_id(cls, answer_id) -> "Answer":
        return cls.objects.get(id=answer_id)
