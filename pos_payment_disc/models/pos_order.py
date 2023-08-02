# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PosOrder(models.Model):
    _inherit = "pos.order"
    
    discount_move_id = fields.Many2one('account.move', string='Discount Move',copy=False)
    
    
    def show_journal_items(self):
        self.ensure_one()
        all_related_moves = self.discount_move_id
        return {
            'name': _('Journal Items'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.line',
            'view_mode': 'tree',
            'view_id':self.env.ref('account.view_move_line_tree_grouped').id,
            'domain': [('id', 'in', all_related_moves.mapped('line_ids').ids)],
            'context': {
                'journal_type':'general',
                'search_default_group_by_move': 1,
                'group_by':'move_id', 'search_default_posted':1,
                'name_groupby':1,
            },
        }
    
    def action_pos_order_paid(self):
        res = super(PosOrder, self).action_pos_order_paid()
        for order in self:
            if 'refund' in order.name.lower():    
                move_lines_data = []
                discount_journal_id = False
                for payment in order.payment_ids.filtered(lambda p:p.payment_method_id.apply_discount):
                    discount_journal_id = payment.payment_method_id.discount_journal_id
                    move_lines_data.append((0,0,{
                            'name': order.name+" | Discount Adjustment",
                            'account_id': payment.payment_method_id.receivable_disc_account_id.id,
                            'debit': 0,
                            'credit': -1*payment.amount*(payment.payment_method_id.receivable_discount/100),
                        }))
                    move_lines_data.append(
                            (0,0,{
                            'name': order.name+" | Discount Adjustment",
                            'account_id': payment.payment_method_id.expense_disc_account_id.id,
                            'debit': -1*payment.amount*(payment.payment_method_id.receivable_discount/100),
                            'credit': 0,
                        }))
                if discount_journal_id:
                    move_id  = self.env['account.move'].create({
                        'date':fields.Date.today(),
                        'journal_id': discount_journal_id.id,
                        'line_ids': move_lines_data})
                    order.discount_move_id = move_id
                    if move_id:
                        move_id.action_post()
        return res

    
    @api.model
    def _process_order(self, order, draft, existing_order):
        order_id = super(PosOrder,self)._process_order(order, draft, existing_order)
        pos_order_id = self.env['pos.order'].browse(order_id)
        if pos_order_id and 'refund' not in pos_order_id.name.lower():
            move_lines_data = []
            discount_journal_id = False
            total_without_discount = sum(pos_order_id.lines.filtered\
                    (lambda l:l.price_subtotal_incl > 0).mapped('price_subtotal_incl'))
            for payment in pos_order_id.payment_ids.filtered(lambda p:p.payment_method_id.apply_discount):
                discount_journal_id = payment.payment_method_id.discount_journal_id
                move_lines_data.append((0,0,{
                        'name': pos_order_id.name+" | Discount Adjustment",
                        'account_id': payment.payment_method_id.receivable_disc_account_id.id,
                        'debit': total_without_discount*(payment.payment_method_id.receivable_discount/100),
                        'credit': 0,
                    }))
                move_lines_data.append(
                        (0,0,{
                        'name': pos_order_id.name+" | Discount Adjustment",
                        'account_id': payment.payment_method_id.expense_disc_account_id.id,
                        'debit': 0,
                        'credit': total_without_discount*(payment.payment_method_id.receivable_discount/100),
                    }))
            if discount_journal_id:
                move_id  = self.env['account.move'].create({
                    'date':fields.Date.today(),
                    'journal_id': discount_journal_id.id,
                    'line_ids': move_lines_data})
                pos_order_id.discount_move_id = move_id
                if move_id:
                    move_id.action_post()
        return order_id
            
            