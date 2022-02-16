from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from quizzes.serializers import (
    ParticipationSerializerInput,
    AnswerSerializerOutput,
)
from rest_framework_simplejwt.views import token_verify
from rest_framework import status, authentication, permissions
from quizzes.models import Participation
from quizzes.serializers import UserParticipationsSerializerOutput
from quizzes.serializers import QuizSerializerOutput

PARTICIPATION_NOT_FOUND = "Participations was not found"
UNAUTHORIZED_PARTICIPATION = "You don't have access to this participation"


class ParticipateAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        user = request.user
        user_id = user.id
        participation_data = {"user": user_id, "quiz": quiz_id}
        serializer = ParticipationSerializerInput(data=participation_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ParticipationAnswersAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, participation_id):

        user = request.user
        user_id = user.id
        participation = Participation.get_participation_by_id(participation_id)

        # check if there is a participation
        if participation is None:
            return Response(
                {"message": PARTICIPATION_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if the participation belongs to the user
        if participation.user_id != user_id:
            return Response(
                {"message": UNAUTHORIZED_PARTICIPATION},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        answers = participation.answers
        serializer = AnswerSerializerOutput(answers, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserParticipationsAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        filter_value = request.GET.get("filter")
        user = request.user
        participations = user.participations

        # if there is a filter value, filter the participations by the quiz name
        if filter_value:
            participations = participations.filter(quiz__name__contains=filter_value)

        serializer = UserParticipationsSerializerOutput(participations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParticipationProgressAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, participation_id):

        user = request.user
        user_id = user.id
        participation = Participation.get_participation_by_id(participation_id)

        # check if there is a participation
        if participation is None:
            return Response(
                {"message": PARTICIPATION_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if the participation belongs to the user
        if participation.user_id != user_id:
            return Response(
                {"message": UNAUTHORIZED_PARTICIPATION},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({"progress": participation.progress}, status=status.HTTP_200_OK)


class ParticipationQuizAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, participation_id):

        participation = Participation.get_participation_by_id(participation_id)

        # check if there is a participation
        if participation is None:
            return Response(
                {"message": PARTICIPATION_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = QuizSerializerOutput(participation.quiz)

        return Response(serializer.data, status=status.HTTP_200_OK)
