from django.db import models
from django.conf import settings
import uuid
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from io import BytesIO
from http.client import HTTPResponse


class Headline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='logo', name='headline-logo', blank=True, null=True)
    header_img = models.ImageField(upload_to='header_image', name='headline-image', blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    allow_vote_changes = models.BooleanField(default=True)
    require_google_auth = models.BooleanField(default=False, help_text="Require Google OAuth authentication to vote")
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def get_creator(self):
        return self.creator.nickname
    
    def process_image(self, image_field, desired_size, format='PNG', quality=90):
        if not image_field:
            return  HTTPResponse(status=204)
        img = Image.open(image_field)
        img.thumbnail(desired_size)
        width, height = img.size
        left = (width - desired_size[0]) / 2
        top = (height - desired_size[1]) / 2
        right = (width + desired_size[0]) / 2
        bottom = (height + desired_size[1]) / 2
        img = img.crop((left, top, right, bottom))
        img_output = BytesIO()
        img = img.convert("RGB")
        img.save(img_output, format=format, quality=quality)
        img_output.seek(0)
        extension = f"{image_field.name.split('.')[0]}_cropped.{format.lower()}"
        processed_image = InMemoryUploadedFile(
            img_output, 'ImageField', extension, f'image/{format.lower()}',
            sys.getsizeof(img_output), None
        )
        return processed_image

    def save(self, *args, **kwargs):
        if hasattr(self, 'header_img') and self.header_img:
            self.header_img = self.process_image(self.header_img, (600, 400))

        if hasattr(self, 'logo') and self.logo:
            self.logo = self.process_image(self.logo, (200, 100))
        super().save(*args, **kwargs)


class Poll_information(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=250)
    sub_category = models.CharField(max_length=250)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE, default=1)
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.Name


class Poll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)
    poll_info = models.ForeignKey(Poll_information, on_delete=models.CASCADE)
    pub_date = models.DateField(auto_created=True)
    updated_date = models.DateField(auto_now_add=True)