from invoice.models import Invoice, InvoiceError


class InvoiceCRUD:

    @staticmethod
    def status_issue(invoice: Invoice):
        void_error = invoice.errors.filter(error=InvoiceError.Errors.VOID).first()
        if void_error:
            void_error.delete()
        invoice.status = Invoice.Status.ISSUED
        invoice.save()

    @staticmethod
    def status_sent(invoice: Invoice):
        invoice.status = Invoice.Status.SENT
        invoice.save()

    @staticmethod
    def status_paid(invoice: Invoice):
        invoice.status = Invoice.Status.PAID
        past_due_error = invoice.errors.filter(error=InvoiceError.Errors.PAST_DUE).first()
        partially_paid_error = invoice.errors.filter(error=InvoiceError.Errors.PARTIALLY_PAID).first()
        if past_due_error:
            past_due_error.delete()
        if partially_paid_error:
            partially_paid_error.delete()
        invoice.save()

    @staticmethod
    def error_past_due(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.PAST_DUE).first()
        if error:
            return
        InvoiceError.objects.create(
                invoice=invoice,
                error=InvoiceError.Errors.PAST_DUE,
                level=InvoiceError.Levels.CRITICAL,
                )

    @staticmethod
    def error_void(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.VOID).first()
        if error:
            return
        InvoiceError.objects.create(
                invoice=invoice,
                error=InvoiceError.Errors.VOID,
                level=InvoiceError.Levels.WARN,
                )
        past_due_error = invoice.errors.filter(error=InvoiceError.Errors.PAST_DUE).first()
        if past_due_error:
            past_due_error.delete()
        invoice.status = Invoice.Status.DRAFT
        invoice.save()


    @staticmethod
    def error_refund(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.REFUNDED).first()
        if error:
            return
        InvoiceError.objects.create(
                invoice=invoice,
                error=InvoiceError.Errors.REFUNDED,
                level=InvoiceError.Levels.ERROR,
                )
        past_due_error = invoice.errors.filter(error=InvoiceError.Errors.PAST_DUE).first()

        if past_due_error:
            past_due_error.delete()
        invoice.status = Invoice.Status.DRAFT
        invoice.save()

    @staticmethod
    def clear_modified(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.MODIFIED).first()
        if error:
            error.delete()

    @staticmethod
    def clear_past_due(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.PAST_DUE).first()
        if error:
            error.delete()

    @staticmethod
    def clear_void(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.VOID).first()
        if error:
            error.delete()

    @staticmethod
    def clear_refund(invoice: Invoice):
        error = invoice.errors.filter(error=InvoiceError.Errors.REFUNDED).first()
        if error:
            error.delete()
