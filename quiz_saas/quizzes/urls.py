from django.urls import path

from . import apis

urlpatterns = [
    path("quizzes", apis.QuizzesAPI.as_view()),
    path("quizzes/<int:quiz_id>/scores", apis.QuizScoresAPI.as_view()),
    path("quizzes/<int:quiz_id>/participate", apis.ParticipateAPI.as_view()),
    path(
        "participations/<int:participation_id>/answers",
        apis.ParticipationAnswersAPI.as_view(),
    ),
    path(
        "participations/<int:participation_id>/answers/<int:answer_id>",
        apis.SelectAnswerAPI.as_view(),
    ),
    path(
        "participations",
        apis.UserParticipationsAPI.as_view(),
    ),
    path(
        "participations/<int:participation_id>/progress",
        apis.ParticipationProgressAPI.as_view(),
    ),
    path(
        "participations/<int:participation_id>/quiz",
        apis.ParticipationQuizAPI.as_view(),
    ),
    path(
        "invite/<int:quiz_id>",
        apis.SendEmailAPI.as_view(),
    ),
    path(
        "invitations/<str:invitation_id>",
        apis.AcceptInvitationAPI.as_view(),
    ),
    path(
        "search",
        apis.SearchAPI.as_view(),
    ),
]
