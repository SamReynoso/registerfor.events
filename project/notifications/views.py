from django.db.models import Count
from django.shortcuts import render
from notifications.models import Alerts, Conversation, DirectMessage
from models.models import Profile


def alerts_view(request):
    alerts = Alerts.objects.filter(recipient=request.user.profile)

    new_alerts = list(alerts.filter(is_read=False))
    alerts.filter(id__in=[a.id for a in new_alerts]).update(is_read=True)

    old_alerts = alerts.filter(is_read=True)

    context = {
        'new_alerts': new_alerts,
        'old_alerts': old_alerts,
    }

    return render(request, 'notifications/alerts.html', context)


def announcements_view(request):
    return render(request, 'notifications/announcements.html')


def notifications_view(request):
    return render(request, 'notifications/notifications.html')


def direct_messages_view(request):
    conversations = Conversation.objects.filter(
            participants=request.user.profile).all()
    context = {'conversations': conversations}
    return render(request, 'notifications/direct_messages.html', context)


def get_convo_helper(sender: Profile, recipient: Profile) -> Conversation:
    convo = (
            Conversation.objects
            .filter(participants=sender)
            .filter(participants=recipient)
            .annotate(num=Count('participants'))
            .filter(num=2)
            .first()
            )

    if convo is None:
        convo = Conversation.objects.create()
        convo.participants.add(sender)
        convo.participants.add(recipient)
        convo.save()
    convo.refresh_from_db()
    return convo


def conversation_view(request, profile_id: int):
    sender = request.user.profile
    recipient = Profile.objects.get(id=profile_id)
    convo = get_convo_helper(sender, recipient)

    if request.method == 'POST':
        body = request.POST.get('body')
        DirectMessage.objects.create(conversation=convo,
                                     body=body,
                                     sender=sender)
        convo.refresh_from_db()
    context = {
            'sender': sender,
            'conversation': convo,
            }
    return render(request, 'notifications/conversation.html', context)
