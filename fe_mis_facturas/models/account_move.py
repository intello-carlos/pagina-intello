from odoo import api, fields, models, _, exceptions


class AccountMove(models.Model):
    _inherit = 'account.move'

    def send_document(self):
        super(AccountMove, self).send_document()
        fe_methods = self.env['fe.mf.methods']
        fe_methods.send_electronic_document(self)

    def send_gr_document(self, b64):
        fe_methods = self.env['fe.mf.methods']
        fe_methods.send_rg_electronic_document(b64, self)
        self.update_electronic_document_status(6)

    def cron_electronic_invoice(self):
        invoices = super(AccountMove, self).cron_electronic_invoice()
        fe_methods = self.env['fe.mf.methods']
        parameter = fe_methods._get_parameters_connection()
        parameter_settings = fe_methods._get_parameters_settings()

        if invoices:
            for invoice in invoices:
                if invoice.electronic_document_status != 0:
                    # invoice_electronic = fe_methods.send_electronic_document(invoice)
                    status_document = fe_methods.get_electronic_document(parameter['url'], parameter['token'], invoice,
                                                                         invoice.send_registry.document_key,
                                                                         document_type=1)
                    print(status_document['DocumentStatus'])
