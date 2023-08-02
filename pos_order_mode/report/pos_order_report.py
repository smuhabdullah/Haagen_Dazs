# -*- coding: utf-8 -*-

from functools import partial

from odoo import models, fields


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    
    order_mode_id = fields.Many2one(comodel_name='pos.modes', string='Order Mode')

    def _select(self):
        return super(PosOrderReport, self)._select() + ',s.order_mode_id AS order_mode_id'

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',s.order_mode_id'
