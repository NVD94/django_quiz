from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions

from quizzes.serializers import (
    QuizSerializerInput,
    ParticipationScoreSerializerOutput,
    QuizSerializerOutput,
)
from quizzes.models import Quiz

UNAUTHORIZED_QUIZ = "You don't own this quiz"
QUIZ_SUCCESS = "Quiz was successfuly created"


class QuizzesAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        quiz_data = request.data
        user = request.user
        user_id = user.id
        quiz_data["user"] = user_id

        serializer = QuizSerializerInput(data=quiz_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": QUIZ_SUCCESS}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):

        user = request.user
        quizzes = user.quizzes
        serializer = QuizSerializerOutput(quizzes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizScoresAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, quiz_id: int):

        quiz_data = request.data
        user_id = request.user.id
        quiz_data["quiz"] = quiz_id

        # get quizz
        quiz = Quiz.get_quiz_by_id(quiz_id)

        # check if quiz belongs to the user
        if quiz.user_id != user_id:
            return Response(
                {"message": UNAUTHORIZED_QUIZ}, status=status.HTTP_401_UNAUTHORIZED
            )

        # get completed participations
        completed_participations = [
            p for p in quiz.participation_list if p.is_completed
        ]

        serializer = ParticipationScoreSerializerOutput(
            completed_participations, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
