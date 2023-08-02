from odoo import models, fields
from datetime import datetime, date
from odoo.tools.safe_eval import dateutil, pytz


class CloseReportWizard(models.TransientModel):
    _name = 'cash.in.out.wizard'

    start_date = fields.Date(string="Start Date", required="True")
    end_date = fields.Date(string="End Date", required="True")
    draft_entries = fields.Boolean('Draft Entries Include')

    def action_print_report(self):
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'draft_entries': self.draft_entries,
            'form': self.read()[0]
        }
        return self.env.ref('cash_bank_in_out_report.report_cash_in_out_id').report_action(self, data=data)


class ReportCard(models.AbstractModel):
    _name = 'report.cash_bank_in_out_report.report_cash_in_out_ids'

    def _get_report_values(self, docids, data=None):
        if data['draft_entries']:
            line_ids = self.env['account.move.line'].search([
                ('date', '>=', data['start_date']),
                ('date', '<=', data['end_date']),
                ('journal_id.type', 'in', ['bank', 'cash']),
                ('account_id.user_type_id.name', '=', 'Bank and Cash'),
                ('move_id.state', '!=', 'cancel')
            ])
        else:
            line_ids = self.env['account.move.line'].search([
                ('date', '>=', data['start_date']),
                ('date', '<=', data['end_date']),
                ('journal_id.type', 'in', ['bank', 'cash']),
                ('account_id.user_type_id.name', '=', 'Bank and Cash'),
                ('move_id.state', '=', 'posted')
            ])

        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            'docs': line_ids,
            'data': data,
            'company': self.env.user.company_id,
        }
