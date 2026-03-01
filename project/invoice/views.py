from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from invoice.models import Invoice
from django.conf import settings
from weasyprint import HTML

from models.models import Event, Registration


def created(request):
    invoices = Invoice.objects.filter(owner=request.user).all()
    context = {'invoices': invoices}
    return render(request, 'invoice/created.html', context)


def events(request):
    events = Event.objects.filter(owner=request.user).all()
    context = {
            'events': events,
               }
    return render(request, 'invoice/events.html', context)


def event_invoices(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    invoices = Invoice.objects.filter(event=event.record).all()
    context = {
            'event': event,
            'invoices': invoices
               }
    return render(request, 'invoice/event_invoices.html', context)


def issue(request, invoice_id: int):
    invoice = __get_invoice(request, invoice_id)
    if invoice is None:
        return HttpResponse(status=403)
    if request.method == 'POST':
        ...
    context = {'invoice': invoice}
    return render(request, 'invoice/issue.html', context)


def issue_event(request, event_id: int):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        ...
    context = {'event': event}
    return render(request, 'invoice/issue_event.html', context)


def preview(request, invoice_id: int):
    invoice = __get_invoice(request, invoice_id)
    if invoice is None:
        return HttpResponse(status=403)
    context = {'invoice': invoice}
    return render(request, 'invoice/preview.html', context)


def received(request):
    invoices = Invoice.objects.filter(owner=request.user).all()
    context = {'invoices': invoices}
    return render(request, 'invoice/issued.html', context)


def __get_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.user != invoice.owner and request.user != invoice.contact:
        return None
    return invoice


def __render_invoice_pdf(invoice):
    total_cost = sum(
            [item.unit_price or 0 for item in invoice.items.all()]
            )

    html_string = render_to_string(
        'invoice/invoice_pdf.html',
        {
            'invoice': invoice,
            'total_cost': total_cost,
            }
    )
    return HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf()


def __get_invoice_response(request, invoice_id, disposition):
    invoice = __get_invoice(request, invoice_id)
    if invoice is None:
        return HttpResponse(status=403)
    pdf = __render_invoice_pdf(invoice)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
            f'{disposition}; filename="invoice_{invoice.id}.pdf"'
            )
    return response


def view_pdf(request, invoice_id):
    return __get_invoice_response(request, invoice_id, 'inline')


def download_pdf(request, invoice_id):
    return __get_invoice_response(request, invoice_id, 'attachment')
