from django.db import models
from django.contrib.auth.models import User
from . import Quiz
import uuid

# _id to access the id of the fk withou querying the database
class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invitee = models.ForeignKey(
        User, related_name="incoming_invitations", on_delete=models.CASCADE
    )

    inviter = models.ForeignKey(
        User, related_name="outgoing_invitations", on_delete=models.CASCADE
    )

    quiz = models.ForeignKey(Quiz, related_name="invitations", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    @classmethod
    def get_invitation_by_id(cls, invitation_id) -> "Invitation":
        return cls.objects.filter(id=invitation_id).first()
