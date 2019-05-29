from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    """Model to store events"""
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=200)
    streamer_id = models.IntegerField()

