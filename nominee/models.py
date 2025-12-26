from django.conf import settings
from django.db import models
from uuid import uuid5
from uuid import uuid4
from voting.models import Headline, Poll_information


class vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    poll_info = models.ForeignKey(Poll_information, on_delete=models.CASCADE)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint( fields=['user', 'headline', 'poll_info'], condition=models.Q(user__isnull=False), name='unique_user_vote_per_poll'),
            models.UniqueConstraint(fields=['ip_address', 'headline', 'poll_info'], condition=models.Q(ip_address__isnull=False), name='unique_ip_vote_per_poll'),
        ]
    
    def __str__(self):
        voter = self.user.username if self.user else f"Anonymous ({self.ip_address})"
        return f"{voter} voted for {self.poll_info.Name}"