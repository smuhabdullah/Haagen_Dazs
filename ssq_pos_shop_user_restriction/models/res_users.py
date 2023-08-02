from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    allowed_pos_config_ids = fields.Many2many(comodel_name="pos.config", string="Allowed POS Shops")
