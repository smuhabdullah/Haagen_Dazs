# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from itertools import groupby

class SessionStockLine(models.Model):
    _name = 'pos.session.stock.line'
    _description = 'Session Stock Session Line'
    _rec_name = 'product_id'

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')
    cost = fields.Float('Cost')
    opening_stock = fields.Float('Opening Stock')
    closing_stock = fields.Float('Closing Stock')
    difference_stock = fields.Float('Difference',compute="compute_difference")
    session_id = fields.Many2one('pos.session', string='Session')

    def compute_difference(self):
        for record in self:
            record.difference_stock = record.opening_stock - record.closing_stock

class PosSession(models.Model):
    _inherit = "pos.session"

    session_stock_ids = fields.One2many('pos.session.stock.line', 'session_id', string='Opening Stock')
    is_session_stock_close = fields.Boolean('Session Stock Closed?',default=False)

    @api.model
    def create(self, vals):
        config_id = self.env['pos.config'].browse(vals['config_id'])
        stock_quants = self.env['stock.quant'].search([\
            ('location_id','child_of',config_id.picking_type_id.default_location_src_id.id),\
            ('show_in_pos_session','=',True)],order='product_id asc')
        session_stock_vals = []
        for product_id, sqs in groupby(stock_quants,key=lambda sq:sq.product_id.id):
            session_stock_vals.append((0,0,{
                    'product_id': product_id,
                    'opening_stock':sum([sq.available_quantity for sq in sqs])
                }))
        vals['session_stock_ids'] = session_stock_vals
        return super(PosSession,self).create(vals)
    