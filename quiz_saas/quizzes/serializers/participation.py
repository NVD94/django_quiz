from rest_framework import serializers
from django.contrib.auth.models import User

from quizzes.models import Participation, Quiz


class ParticipationSerializerInput(serializers.ModelSerializer):
    class Meta:

        model = Participation
        fields = ["user", "quiz"]


class UserParticipationsSerializerOutput(serializers.ModelSerializer):
    class QuizSerializerOutput(serializers.ModelSerializer):
        class Meta:

            model = Quiz
            fields = ["name", "created"]

    quiz = QuizSerializerOutput(read_only=True)
    progress = serializers.ReadOnlyField()

    class Meta:

        model = Participation
        fields = ["id", "quiz", "progress"]


class ParticipationScoreSerializerOutput(serializers.ModelSerializer):
    class UserSerializerOutput(serializers.ModelSerializer):
        class Meta:

            model = User
            fields = ["email"]

    user = UserSerializerOutput(read_only=True)
    score = serializers.ReadOnlyField()

    class Meta:

        model = Participation
        fields = ["score", "user"]
