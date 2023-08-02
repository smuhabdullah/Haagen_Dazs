import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from itertools import groupby

class SessionStockWizard(models.TransientModel):
    _name = 'session.stock.wizard'
    _description = "Session Stock Wizard"


    config_id = fields.Many2one('pos.config', string='Shop')
    opening_stock_line_ids = fields.One2many('session.stock.wizard.line','session_stock_wizard_id', string='Opening Stock Lines')
    type = fields.Selection([
        ('close', 'Close'),
        ('open','Open')
    ], string='type')
    
    @api.onchange('config_id')
    def _onchange_config_id(self):
        if self.type == 'open':
            stock_quants = self.env['stock.quant'].search([\
                ('location_id','child_of',self.config_id.picking_type_id.default_location_src_id.id),\
                ('show_in_pos_session','=',True)],order='product_id asc')
            opening_stock_line_ids = []
            for product_id, sqs in groupby(stock_quants,key=lambda sq:sq.product_id.id):
                product = self.env['product.product'].browse(product_id)
                opening_stock_line_ids.append((0,0,{
                        'product_id': product_id,
                        'product_uom_id': product.uom_id.id if product.uom_id else False,
                        'opening_stock':sum([sq.available_quantity for sq in sqs])
                    }))
            self.update({'opening_stock_line_ids':opening_stock_line_ids})
        else:
            opening_stock_line_ids = []
            sessions = self.env['pos.session'].search([('config_id','=',self.config_id.id)],order='create_date asc')
            for line in sessions[-1].session_stock_ids:
                stock_quants = self.env['stock.quant'].search([\
                    ('location_id','child_of',self.config_id.picking_type_id.default_location_src_id.id),\
                    ('product_id','=',line.product_id.id)],order='product_id asc')
                opening_stock_line_ids.append((0,0,{
                        'product_id': line.product_id.id,
                        'line_id': line.id,
                        'product_uom_id': line.product_id.uom_id.id if line.product_id.uom_id else False,
                        'opening_stock': line.opening_stock,
                        'closing_stock': sum(stock_quants.mapped('available_quantity')),
                        'cost': line.cost
                    }))
            self.update({'opening_stock_line_ids':opening_stock_line_ids})
            
    def action_open_session(self):
        return self.config_id.open_session_cb()
    
    def action_close_session(self):    
        for line in self.opening_stock_line_ids:
            line.line_id.write({
                'closing_stock': line.closing_stock,
                'product_uom_id': line.product_id.uom_id.id if line.product_id.uom_id else False,
                'cost': line.cost
                })
            if abs(line.line_id.difference_stock) > 0:
                self.env['stock.quant'].with_context(inventory_mode=True).create({
                    'location_id': self.config_id.picking_type_id.default_location_src_id.id,
                    'product_id': line.line_id.product_id.id,
                    # 'product_uom_id': line.line_id.product_uom_id.id if line.line_id.product_uom_id else line.line_id.product_id.uom_id.id,
                    'inventory_quantity': line.line_id.closing_stock,
                }).action_apply_inventory()
        sessions = self.env['pos.session'].search([('config_id','=',self.config_id.id)],order='create_date asc')
        if len(sessions) > 0:
            sessions[-1].is_session_stock_close = True

class LeadProductLine(models.TransientModel):
    _name = 'session.stock.wizard.line'

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    product_uom_category_id = fields.Many2one('uom.category', related='product_id.uom_id.category_id')
    line_id = fields.Many2one('pos.session.stock.line', string='Session Stock Line')
    opening_stock = fields.Float('Opening Stock')
    closing_stock = fields.Float('Closing Stock')
    cost = fields.Float('Cost')
    session_stock_wizard_id = fields.Many2one('session.stock.wizard', string='session_stock_wizard')
    

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    
    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        res = super()._get_inventory_fields_create()
        res += ['inventory_quantity']
        return res

    @api.model
    def _get_inventory_fields_write(self):
        """ Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
        """
        res = super()._get_inventory_fields_write()
        res += ['inventory_quantity']
        return res