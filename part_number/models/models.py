# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression


# class Integration(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     portal_allow_api_keys = fields.Char()


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    part_no = fields.Char('Part #')

    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name', 'default_code'])
        return [(template.id, '%s%s%s' % (template.default_code and '[%s] ' % template.default_code or '', template.name, template.part_no and ' [%s]' % template.part_no or ''))
                for template in self]


class ProductProductInh(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        res = []
        for rec in self:
            if rec.part_no:
                res.append((rec.id, '[%s] %s [%s]' % (rec.default_code or '', rec.name, rec.part_no or '')))
            else:
                res.append((rec.id, '[%s] %s' % (rec.default_code or '', rec.name)))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        name search that supports searching by tag code
        """
        args = args or []
        domain = []
        if name:
            domain = ['|', '|',('part_no', '=ilike', name + '%'), ('name', operator, name), ('default_code', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&'] + domain
        state = self.search(domain + args, limit=limit)
        return state.name_get()



