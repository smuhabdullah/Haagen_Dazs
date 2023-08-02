# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Product(models.Model):
    _inherit = 'product.template'

    show_in_pos_session = fields.Boolean('Show In POS Session',default=False)

class ProductQuant(models.Model):
    _inherit = 'stock.quant'

    show_in_pos_session = fields.Boolean('Show In POS Session',related='product_id.show_in_pos_session')

