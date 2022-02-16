from rest_framework import serializers

from quizzes.models import Answer


class AnswerSerializerInput(serializers.ModelSerializer):
    class Meta:

        model = Answer
        fields = ["content", "is_correct"]


class AnswerSerializerOutput(serializers.ModelSerializer):
    class Meta:

        model = Answer
        fields = ["id", "content"]
