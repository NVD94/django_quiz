from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions
from django.core.mail import send_mail

from quizzes.models import Participation, Answer
from quiz_saas.settings import EMAIL_HOST_USER

PARTICIPATION_SUCCESS = "Participation was successfuly completed"
PARTICIPATION_ALREADY_COMPLETED = "Participation was already completed"
UNAUTHORIZED_PARTICIPATION = "You do not have access for this participation"
INVALID_ANSWER = "This answer does not belong to the quiz"
QUESTION_ALREADY_ANSWERED = "This question was already answered"


class SelectAnswerAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, participation_id, answer_id):

        user = request.user
        user_id = user.id
        user_email = user.email
        participation = Participation.get_participation_by_id(participation_id)

        # check if the participation belongs to the user
        if participation.user_id != user_id:
            return Response(
                {"message": UNAUTHORIZED_PARTICIPATION},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # check if the participation is completed
        if participation.is_completed:
            return Response(
                {"message": PARTICIPATION_ALREADY_COMPLETED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        answer = Answer.get_answer_by_id(answer_id)

        # check if the question of the answer actually belongs to the quiz
        is_question_from_quiz = participation.quiz.questions.filter(
            id=answer.question_id
        ).exists()

        if not is_question_from_quiz:
            return Response(
                {"message": INVALID_ANSWER},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the question was already answered, if so remove the previous answer
        preivous_answer = participation.answers.filter(
            question_id=answer.question_id
        ).first()

        if preivous_answer:
            # TODO update the answer
            participation.answers.remove(preivous_answer)

        # save the questions
        participation.answers.add(answer)
        participation.save()

        # check if the participation is completed, if so send and email with the result

        if participation.is_completed:
            res = send_mail(
                (f"Quiz {participation.quiz.name} completed!!"),
                f"Your score is {participation.score}%",
                EMAIL_HOST_USER,
                [user_email],
                fail_silently=False,
            )

        return Response(
            {"message": "Answer successfuly selected"}, status=status.HTTP_201_CREATED
        )
