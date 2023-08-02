# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import random


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"
    
    receivable_discount = fields.Float('Receivable Disc(%)')
    expense_discount = fields.Float('Expense Disc(%)')
    total_discount = fields.Float('Total Disc(%)',store=True)
    apply_discount = fields.Boolean('Apply Discount',default=False)
    discount_product_id = fields.Many2one('product.product', string='Discount Product',domain=[('sale_ok','=',True)])
    receivable_disc_account_id = fields.Many2one('account.account', string='Receivable Account')
    expense_disc_account_id = fields.Many2one('account.account', string='Expense Account')
    discount_journal_id = fields.Many2one('account.journal', string='Journal')
    
    @api.onchange('receivable_discount','expense_discount')
    def _compute_total_discount(self):
        self.total_discount = sum([self.receivable_discount,self.expense_discount])
        
    @api.onchange('receivable_disc_account_id','expense_disc_account_id')
    def _default_discount_product_id(self):
        product = self.env.ref("pos_payment_disc.product_product_payment_discount", raise_if_not_found=False)
        self.discount_product_id = product if product else False

