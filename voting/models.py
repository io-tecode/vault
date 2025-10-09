from django.db import models
from django.conf import settings
import uuid

class Headline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='logo', name='headline-logo')
    header_img = models.ImageField(upload_to='header_image', name='headline-image')
    creation_date = models.DateField(auto_created=True)
    updated_date = models.DateField(auto_now_add=True)


class Poll_information(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=250)
    sub_category = models.CharField(max_length=250)


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)
    poll_info = models.ForeignKey(Poll_information, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_created=True)
    updated_date = models.DateField(auto_now_add=True)

class Option(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    opttext = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.opttext
    

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'poll') 


