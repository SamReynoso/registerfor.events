from django.shortcuts import render
from notifications.models import Conversation
from models.models import Profile


def announcements(request):
    return render(request, 'notifications/announcements.html')


def notifications(request):
    return render(request, 'notifications/notifications.html')


def direct_messages(request):
    conversations = Conversation.objects.filter(participants=request.user).all()
    context = {'conversations': conversations}
    return render(request, 'notifications/direct_messages.html', context)


def conversation_view(request, profile_id: int):
    recipient = Profile.objects.get(id=profile_id)
    sender = request.user.profile
    qs = Conversation.objects.all()
    for p_id in [recipient.id, sender.id]:
        qs.filter(participants__id=p_id)
    convo = qs.first()
    if convo is not None:
        msgs = convo.direct_messages.all()
    else:
        msgs = []

    context = {
            'recipient': recipient,
            'messages': msgs,
            }
    return render(request, 'notifications/conversation.html', context)
