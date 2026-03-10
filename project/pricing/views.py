from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from invoice.models import Invoice
from django.conf import settings
from weasyprint import HTML

from models.forms import EventPriceForm
from models.models import Division, Event, Registration


def pricing(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {
            'event': event,
            }
    return render(request, 'pricing/pricing.html', context)

def default(request, event_id: int):
    event = Event.objects.get(id=event_id)
    form = EventPriceForm(instance=event)
    context = {
            'event': event,
            'form': form,
            }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            divisions = Division.objects.filter(event=event)
            for division in divisions:
                division.unit_price = event.unit_price
                division.save()
                items = Registration.items.all()
                for item in items:
                    item.unit_price = event.unit_price
                    item.save()
    return render(request, 'pricing/default.html', context)

def divisions(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {
            'event': event,
            }
    return render(request, 'pricing/divisions.html', context)

def discounts(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {
            'event': event,
            }
    return render(request, 'pricing/discounts.html', context)

def registrations(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {
            'event': event,
            }
    return render(request, 'pricing/registrations.html', context)
