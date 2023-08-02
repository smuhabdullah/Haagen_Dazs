from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    strn = fields.Char('Strn')

class CompanyInherit(models.Model):
    _inherit = 'res.company'

    strn = fields.Char('Strn')