
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    is_session_stock_close = fields.Boolean('Session Stock Closed?',compute="is_session_close")
    
    def is_session_close(self):
        for config in self:
            sessions = self.env['pos.session'].search([('config_id','=',config.id)],order='create_date asc')
            if sessions:
                config.is_session_stock_close = sessions[-1].is_session_stock_close
            else:
                config.is_session_stock_close = True

    def open_session_cb_stock(self):
        self.ensure_one()
        return {
            'name': _('Opening Session Stock'),
            'res_model': 'session.stock.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_type':'open','default_config_id': self.id}
        }
    def close_session_cb_stock(self):
        self.ensure_one()
        return {
            'name': _('Closing Session Stock'),
            'res_model': 'session.stock.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_type':'close','default_config_id': self.id}
        }