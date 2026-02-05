from django.conf import settings
from django.db import models
from models.models import Event, Profile


class Conversation(models.Model):
    participants = models.ManyToManyField(Profile,
                                          related_name='conversations')


class DirectMessage(models.Model):
    conversation = models.ForeignKey(
            Conversation,
            on_delete=models.CASCADE,
            related_name='direct_messages')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Announcement(models.Model):
    sender = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            related_name='sent_announcements')
    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='announcements')
    title = models.CharField(max_length=255)
    body = models.TextField()
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient}: {self.title}"


class Notification(models.Model):
    sender = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            related_name='sent_notifications')
    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient}: {self.title}"
