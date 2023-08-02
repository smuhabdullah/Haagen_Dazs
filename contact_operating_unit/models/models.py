# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _default_operating_unit_ids(self):
        if self.env.user.default_operating_unit_id:
            return [
                (
                    6,
                    0,
                    [self.env["res.users"].operating_unit_default_get(self.env.uid).id],
                )
            ]

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        string="Operating Units",
        default=_default_operating_unit_ids,
    )
