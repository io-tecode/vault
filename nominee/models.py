from django.conf import settings
from django.db import models
from uuid import uuid5
from uuid import uuid4
from voting.models import Headline, Poll_information

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll_info = models.ForeignKey(Poll_information, on_delete=models.CASCADE)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll_info', 'headline')

    def __str__(self):
        return f"{self.user.username} voted for {self.poll_info.Name} in {self.headline.title}"