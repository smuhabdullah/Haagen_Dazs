from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    
    _inherit = 'pos.order'
    
    order_mode_id = fields.Many2one(comodel_name='pos.modes', string='Order Mode')
    
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['order_mode_id'] = ui_order.get('order_mode_id', False)
        return order_fields
    