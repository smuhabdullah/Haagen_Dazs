# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class OperatingUnitInh(models.Model):
    _inherit = "operating.unit"

    seq_no = fields.Char('Sequence No', required=True, copy=False)
    last_no = fields.Integer('Last No', copy=False)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("operating_unit_ids")
    def onchange_operating_unit(self):
        for record in self:
            if len(record.operating_unit_ids.ids) > 1:
                raise UserError('You cannot select operating unit greater than one.')

    @api.model
    def create(self, vals_list):
        record = super().create(vals_list)
        if record.operating_unit_ids:
            unit = record.operating_unit_ids[0]
            unit.last_no += 1
            code = unit.seq_no + record.make_four_digit(unit.last_no)
            record.default_code = code
        return record

    def write(self, vals_list):
        record = super().write(vals_list)
        if 'operating_unit_ids' in vals_list and self.operating_unit_ids:
            unit = self.operating_unit_ids[0]
            unit.last_no += 1
            code = unit.seq_no + self.make_four_digit(unit.last_no)
            self.default_code = code
        return record

    def make_four_digit(self, seq):
        if seq < 10:
            ss = '000' + str(seq)
        elif seq >= 10 and seq < 100:
            ss = '00' + str(seq)
        elif seq >= 100 and seq < 1000:
            ss = '0' + str(seq)
        else:
            ss = str(seq)
        return ss
