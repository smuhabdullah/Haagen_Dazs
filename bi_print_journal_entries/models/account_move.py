# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    posting_date = fields.Datetime('Posting Date')

    def action_post(self):
        res = super(AccountMove, self).action_post()
        self.posting_date = datetime.datetime.now()
        return res
