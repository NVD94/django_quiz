from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions
from django.core.mail import send_mail

from django.contrib.auth.models import User
from quizzes.serializers import ParticipationSerializerInput
from quizzes.serializers import InvitationSerializerInput
from quizzes.models import Invitation
from quiz_saas.settings import EMAIL_HOST_USER

INVITATION_SEND_SUCCESS = "Invitation was successfully sent"
USER_ALREAD_INVITED = "The user was already invited to the quiz"
EMAIL_SEND_ERROR = "Failed to send an email, therefore the user was not invited"
BASE_INVITATION_URL = "http://127.0.0.1:8000/invitations/"
INVALID_INVITATION = "This invitation is invalid"
INVITATION_ALREADY_ACCEPTED = "This invitation was already accepted"
INVITATION_ACCEPT_SUCCES = "This invitation was successfuly accepted"


class SendEmailAPI(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):

        data = request.data
        user = request.user
        user_id = user.id
        user_email = user.email
        invitation_email = data.pop("email")

        # get invited user object
        invited_user = User.objects.filter(email=invitation_email).first()
        data["inviter"] = user_id
        data["invitee"] = invited_user.id
        data["quiz"] = quiz_id

        # check if the user that was invited exists
        if invited_user is None:
            return Response(
                {"message": f"No user was found with email{invitation_email}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # check if user was already invited
        was_already_invited = invited_user.incoming_invitations.filter(quiz_id=quiz_id)
        if was_already_invited:
            return Response(
                {"message": USER_ALREAD_INVITED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = InvitationSerializerInput(data=data)
        if serializer.is_valid(raises_exception=True):
            invitation_object = serializer.save()
            res = send_mail(
                (user_email + "invited to join a quiz"),
                BASE_INVITATION_URL + str(invitation_object.id),
                EMAIL_HOST_USER,
                [invitation_email],
                fail_silently=False,
            )
            # check if the email was successfully sent
            if res != 1:
                invitation_object.delete()
                return Response(
                    {"message": EMAIL_SEND_ERROR},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": INVITATION_SEND_SUCCESS}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AcceptInvitationAPI(APIView):
    def get(self, request, invitation_id):

        # get invitation
        invitation = Invitation.get_invitation_by_id(invitation_id)

        # check invitation if exists
        if invitation is None:
            return Response(
                {"message": INVALID_INVITATION},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if was already accepted
        if invitation.accepted:
            return Response(
                {"message": INVITATION_ALREADY_ACCEPTED},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # change invitation accepted to true
        invitation.accepted = True
        invitation.save()
        return Response(
            {"message": INVITATION_ACCEPT_SUCCES}, status=status.HTTP_204_NO_CONTENT
        )
