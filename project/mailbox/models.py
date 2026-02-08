from django.conf import settings
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Alert(models.Model):
    target = GenericForeignKey("content_type", "object_id")

    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='alerts')
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    body = models.TextField()

    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient}: {self.title}"


class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name='conversations')


class DirectMessage(models.Model):
    conversation = models.ForeignKey(
            Conversation,
            on_delete=models.CASCADE,
            related_name='direct_messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='sent_direct_messages')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# class Announcement(models.Model):
#     sender = models.ForeignKey(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.SET_NULL,
#             null=True,
#             related_name='sent_announcements')
#     recipient = models.ForeignKey(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.CASCADE,
#             related_name='announcements')
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     event = models.ForeignKey(Event,
#                               on_delete=models.CASCADE,
#                               null=True,
#                               blank=True)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"To {self.recipient}: {self.title}"
#

# class Notification(models.Model):
#     sender = models.ForeignKey(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.SET_NULL,
#             null=True,
#             related_name='sent_notifications')
#     recipient = models.ForeignKey(
#             settings.AUTH_USER_MODEL,
#             on_delete=models.CASCADE,
#             related_name='notifications')
#     event = models.ForeignKey(Event,
#                               on_delete=models.CASCADE,
#                               null=True,
#                               blank=True)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"To {self.recipient}: {self.title}"
