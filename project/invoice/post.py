from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from invoice.invoices import InvoiceCRUD
from invoice.models import Invoice

def reset(request, invoice_id: int):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.status = Invoice.Status.DRAFT
    invoice.save()
    url = reverse('invoice:preview', args=[invoice.id])
    return redirect(url)

def status_page(request, invoice_id: int, func, temp, context={}):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    if request.method == 'POST':
        func(invoice)
        url = reverse('invoice:preview', args=[invoice.id])
        return redirect(f'{url}#lifecycle')
    context['invoice'] = invoice
    return render(request, temp, context)


@login_required(login_url='/login/')
def status_issue(request, invoice_id: int):
    context = {'title': 'Issue Invoice'}
    return status_page(request,
                       invoice_id,
                       InvoiceCRUD.status_issue,
                       'invoice/post/status_issue.html',
                       context=context
                       )


@login_required(login_url='/login/')
def status_sent(request, invoice_id: int):
    context = {'title': 'Send'}
    return status_page(request,
                       invoice_id,
                       InvoiceCRUD.status_sent,
                       'invoice/post/status_sent.html',
                       context=context
                       )

@login_required(login_url='/login/')
def status_paid(request, invoice_id: int):
    context = {'title': 'Make Paid'}
    return status_page(request,
                       invoice_id,
                       InvoiceCRUD.status_paid,
                       'invoice/post/status_paid.html',
                       context=context
                       )

@login_required(login_url='/login/')
def error_past_due(request, invoice_id: int):
    context = {'title': 'Flag Past Due'}
    return status_page(request,
                       invoice_id,
                       InvoiceCRUD.error_past_due,
                       'invoice/post/error_past_due.html',
                       context=context,
                       )


@login_required(login_url='/login/')
def error_void(request, invoice_id: int):
    context = {'title': 'Void Invoice'}
    return status_page(request,
                       invoice_id,
                       InvoiceCRUD.error_void,
                       'invoice/post/error_void.html',
                       context=context,
                       )


@login_required(login_url='/login/')
def error_refund(request, invoice_id: int):
    context = {'title': 'Void Invoice'}
    return status_page(request,
                       invoice_id,
                       InvoiceCRUD.error_refund,
                       'invoice/post/error_refund.html',
                       context=context,
                       )

def clear_route(request, invoice_id: int, func):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.owner != request.user:
        return HttpResponseForbidden("You don't own this event.")
    func(invoice)
    url = reverse('invoice:preview', args=[invoice.id])
    return redirect(f'{url}#lifecycle')


@login_required(login_url='/login/')
def clear_modified(request, invoice_id: int):
    return clear_route(request, invoice_id, InvoiceCRUD.clear_modified)

@login_required(login_url='/login/')
def clear_past_due(request, invoice_id: int):
    return clear_route(request, invoice_id, InvoiceCRUD.clear_past_due)

@login_required(login_url='/login/')
def clear_void(request, invoice_id: int):
    return clear_route(request, invoice_id, InvoiceCRUD.clear_void)

@login_required(login_url='/login/')
def clear_refund(request, invoice_id: int):
    return clear_route(request, invoice_id, InvoiceCRUD.clear_refund)



