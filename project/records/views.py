from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from records.models import Invoice, RegistrationRecord
from django.conf import settings
from weasyprint import HTML


def records(request):
    invoices = Invoice.objects.filter(owner=request.user).all()
    context = {'invoices': invoices}
    return render(request, 'records/records.html', context)


def invoices(request):
    invoices = Invoice.objects.filter(owner=request.user).all()
    context = {'invoices': invoices}
    return render(request, 'records/invoices.html', context)


def invoice_details(request, invoice_id: int):
    invoice = get_invoice(request, invoice_id)
    if invoice is None:
        return HttpResponse(status=403)
    context = {'invoice': invoice}
    return render(request, 'records/invoice_details.html', context)


def registrations(request):
    registrations = RegistrationRecord.objects.filter(owner=request.user).all()
    context = {'registrations': registrations}
    return render(request, 'records/registrations.html', context)


def get_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.user != invoice.owner and request.user != invoice.contact:
        return None
    return invoice


def render_invoice_pdf(invoice):
    total_cost = sum(
            [rec.unit_price for rec in invoice.registration_records.all()]
            )

    html_string = render_to_string(
        'records/invoice_pdf.html',
        {
            'invoice': invoice,
            'total_cost': total_cost,
            }
    )
    return HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf()


def get_invoice_response(request, invoice_id, disposition):
    invoice = get_invoice(request, invoice_id)
    if invoice is None:
        return HttpResponse(status=403)
    pdf = render_invoice_pdf(invoice)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
            f'{disposition}; filename="invoice_{invoice.id}.pdf"'
            )
    return response


def view_invoice(request, invoice_id):
    return get_invoice_response(request, invoice_id, 'inline')


def download_invoice(request, invoice_id):
    return get_invoice_response(request, invoice_id, 'attachment')


def send_invoice_email(invoice):
    ...


