from http.client import UNAUTHORIZED
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions

from quizzes.serializers import (
    ParticipationScoreSerializerOutput,
    QuizSerializerOutput,
    QuizSimpleSerializerOutput,
)
from quizzes.models import Quiz

UNAUTHORIZED_QUIZ = "You don't own this quiz"


def _get_user_created_answers(user):
    quizzes = user.quizzes
    pass


class SearchAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = request.user
        filter_value = request.GET.get("filter")
        # TODO Browse quizzes, participants, invitees, answers,... - search, filter,...

        # filter quizzes names

        quizzes = user.quizzes

        # get the invitation that were already acceped aka invitation from the participants
        participants_invts = user.outgoing_invitations.filter(accepted=True)

        # get the pending invitations aka invitations from invitees
        invitees_invts = user.outgoing_invitations.filter(accepted=False)

        # get all answers from the quizzes
        if filter_value:
            quizzes = quizzes.filter(name__contains=filter_value)
        # participants_invts = participants_invts.filter(user__email=filter_value)
        # invitees_invts = invitees_invts.filter(user__email=filter_value)
        quiz_serializer = QuizSimpleSerializerOutput(quizzes, many=True)
        # filter participants

        # answers

        # questions
        response_data = {"quizzes": quiz_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)
