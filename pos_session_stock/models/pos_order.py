# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def open_session_stock(self):
        ctx = dict(
            default_config_id=self.id
            )
        return {
            'name': _('Session Stock Wizard'),
            'res_model': 'session.stock.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',  
            'context': ctx,
            }