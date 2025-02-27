from django.db import models

from apps.core.mixinx import EncryptMixin


class Channel(models.Model, EncryptMixin):
    name = models.CharField(max_length=100)
    channel_type = models.CharField(max_length=100)
    config = models.JSONField(default=dict)
    description = models.TextField()


class ChannelTemplate(models.Model):
    name = models.CharField(max_length=100)
    channel_obj = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.TextField()
    app = models.CharField(max_length=100)
    context = models.TextField()
