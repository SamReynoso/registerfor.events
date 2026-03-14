from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from invoice.models import Invoice
from django.conf import settings
from weasyprint import HTML

from models.forms import DivisionPriceForm, EventPriceForm, RegistrationItemPriceForm, RegistrationPriceForm
from models.models import Division, Event, Registration, RegistrationItem


def pricing(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {
            'event': event,
            }
    return render(request, 'pricing/pricing.html', context)

def default(request, event_id: int):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventPriceForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            for division in event.divisions.all():
                division.unit_price = event.unit_price
                division.save()
                for item in division.items.all():
                    item.unit_price = event.unit_price
                    item.save()
        return redirect('pricing:pricing', event_id=event.id)
    else:
        form = EventPriceForm(instance=event)

    context = {
            'event': event,
            'form': form,
            }
    return render(request, 'pricing/default.html', context)

def divisions(request, event_id: int):
    event = Event.objects.get(id=event_id)
    context = {
            'event': event,
            }
    return render(request, 'pricing/divisions.html', context)

def division(request, division_id: int):
    division = Division.objects.get(id=division_id)
    if request.method == 'POST':
        form = DivisionPriceForm(request.POST, instance=division)
        if form.is_valid():
            form.save()
            for item in division.items.all():
                item.unit_price = division.unit_price
                item.save()
        return redirect('pricing:pricing', event_id=division.event.id)
    else:
        form = DivisionPriceForm(instance=division)
    context = {
            'division': division,
            'form': form,
            }
    return render(request, 'pricing/division.html', context)


def registration(request, registration_id: int):
    registration = Registration.objects.get(id=registration_id)
    if request.method == 'POST':
        form = RegistrationPriceForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            for item in registration.items.all():
                item.unit_price = registration.unit_price
                item.save()
        return redirect('pricing:pricing', event_id=registration.event.id)
    else:
        form = RegistrationPriceForm(instance=registration)
    context = {
            'registration': registration,
            'form': form,
            }
    return render(request, 'pricing/registration.html', context)


def registration_item(request, registration_item_id: int):
    item = RegistrationItem.objects.get(id=registration_item_id)
    if request.method == 'POST':
        form = RegistrationItemPriceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect('pricing:pricing', event_id=item.registration.event.id)
    else:
        form = RegistrationItemPriceForm(instance=item)
    context = {
            'item': item,
            'form': form,
            }
    return render(request, 'pricing/registration_item.html', context)


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
