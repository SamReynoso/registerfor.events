from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from django.db.models import Count
from mailbox.models import Alert, Conversation, DirectMessage
from models.models import Announcement


def alerts_view(request):
    alerts = Alert.objects.filter(recipient=request.user)
    if request.method == 'POST':
        alerts.delete()

    new_alerts = list(alerts.filter(is_read=False))
    old_alerts = list(alerts.filter(is_read=True))

    alerts.filter(id__in=[a.id for a in new_alerts]).update(is_read=True)
    context = {
            'new_alerts': new_alerts,
            'old_alerts': old_alerts,
            }
    return render(request, 'mailbox/alerts.html', context)


def announcements_view(request):
    announcements = Announcement.objects.filter(recipient=request.user).all()
    announcements = Announcement.objects.all()
    context = {'announcements': announcements}
    return render(request, 'mailbox/announcements.html', context)


def announcement_view(request, announcement_id: int):
    announcement = Announcement.objects.get(id=announcement_id)
    context = {'announcement': announcement}
    return render(request, 'mailbox/announcement.html', context)


def mailbox(request):
    return render(request, 'mailbox/mailbox.html')


def direct_messages_view(request):
    conversations = Conversation.objects.filter(
            participants=request.user).all()
    context = {'conversations': conversations}
    return render(request, 'mailbox/direct_messages.html', context)


def get_convo_helper(sender, recipient) -> Conversation:
    convo = (
            Conversation.objects
            .filter(participants=sender)
            .filter(participants=recipient)
            .first()
            )

    if convo is None:
        convo = Conversation.objects.create()
        convo.participants.add(sender)
        convo.participants.add(recipient)
        convo.save()
    return convo


def conversation_view(request, user_id: int):
    sender = request.user
    User = get_user_model()
    recipient = User.objects.get(id=user_id)
    convo = get_convo_helper(sender, recipient)

    if request.method == 'POST':
        body = request.POST.get('body')
        DirectMessage.objects.create(conversation=convo,
                                     body=body,
                                     sender=sender)
        convo.refresh_from_db()
    context = {
            'sender': sender,
            'recipient': recipient,
            'conversation': convo,
            }
    return render(request, 'mailbox/conversation.html', context)


def conversation_delete_view(request, user_id: int):
    sender = request.user
    User = get_user_model()
    recipient = User.objects.get(id=user_id)
    convo = get_convo_helper(sender, recipient)
    if request.method == 'POST':
        convo.delete()
        print('convo deleted')
        return redirect('mailbox:direct_messages')
    return render(request, 'mailbox/conversation_delete.html')

