# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InternalTransferPayment(models.Model):
    _name = 'account.internal.payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Account Internal Payment'

    name = fields.Char(copy=False, index=True, default=lambda self: _('New'))
    amount = fields.Float('Amount')
    is_vendor = fields.Boolean()
    date = fields.Date('Date', default=lambda self: fields.Date.today(), required=True)
    partner_id = fields.Many2one('res.partner')
    move_id = fields.Many2one('account.move', copy=False)
    journal_id = fields.Many2one('account.journal')
    dest_journal_id = fields.Many2one('account.journal')

    state = fields.Selection([('draft', 'Draft'),
                              ('post', 'Posted'),
                              ('cancel', 'Cancel'),
                              ], readonly=True, default='draft', copy=False, string="State", tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('internal.payment.sequence') or _('New')
        result = super(InternalTransferPayment, self).create(vals)
        return result

    def unlink(self):
        for rec in self:
            if rec.move_id:
                raise UserError('You cannot delete payment once its posted.')
            return super().unlink()

    def action_show_jv(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Journal Item',
            'domain': [('ref', '=', self.name)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }

    def action_post(self):
        self.general_entry()
        self.move_id.action_post()
        self.state = 'post'

    def action_draft(self):
        self.state = 'draft'
        self.move_id.button_draft()
        self.move_id.line_ids.unlink()

    def action_cancel(self):
        self.state = 'cancel'
        self.move_id.button_draft()
        self.move_id.button_cancel()

    def general_entry(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        # journal = self.env['account.journal'].search([('code', '=', 'MISC')])
        # if not journal:
        #     raise UserError('Miscellaneous Journal Not Found')
        if not self.move_id:
            move_dict = {
                # 'name': self.move_lines.name,
                'ref': self.name,
                'journal_id': self.journal_id.id,
                'partner_id': self.partner_id.id,
                'date': self.date,
                'state': 'draft',
            }
            debit_line = (0, 0, {
                'name': self.name,
                'debit': abs(self.amount),
                'credit': 0.0,
                'partner_id': self.partner_id.id,
                # 'analytic_account_id': oline.analytic_account_id.id,
                # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                'account_id': self.journal_id.default_account_id.id,
            })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            credit_line = (0, 0, {
                'name': self.name,
                'debit': 0.0,
                'partner_id': self.partner_id.id,
                'credit': abs(self.amount),
                'account_id': self.dest_journal_id.default_account_id.id,
            })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
            move_dict['line_ids'] = line_ids
            move = self.env['account.move'].create(move_dict)
            self.move_id = move.id
            print("General entry created")
        else:
            debit_line = (0, 0, {
                'name': self.name,
                'debit': abs(self.amount),
                'credit': 0.0,
                'partner_id': self.partner_id.id,
                # 'analytic_account_id': oline.analytic_account_id.id,
                # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                'account_id': self.journal_id.default_account_id.id,
            })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            credit_line = (0, 0, {
                'name': self.name,
                'debit': 0.0,
                'partner_id': self.partner_id.id,
                'credit': abs(self.amount),
                'account_id': self.dest_journal_id.default_account_id.id,
            })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
            self.move_id.write({
                'line_ids': line_ids
            })


