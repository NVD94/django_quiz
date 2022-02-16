from rest_framework import serializers
from django.contrib.auth.models import User

from quizzes.models.invitation import Invitation


class InvitationSerializerInput(serializers.ModelSerializer):
    class Meta:

        model = Invitation
        fields = ["invitee", "inviter", "quiz"]
