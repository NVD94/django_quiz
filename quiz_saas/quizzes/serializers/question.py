from rest_framework import serializers

from quizzes.models import Question, Answer
from . import AnswerSerializerInput, AnswerSerializerOutput


class QuestionSerializerInput(serializers.ModelSerializer):
    answers = AnswerSerializerInput(many=True)

    class Meta:

        model = Question
        fields = [
            "content",
            "answers",
        ]


class QuestionSerializerOutput(serializers.ModelSerializer):
    answers = AnswerSerializerOutput(many=True)

    class Meta:

        model = Question
        fields = [
            "id",
            "content",
            "answers",
        ]
