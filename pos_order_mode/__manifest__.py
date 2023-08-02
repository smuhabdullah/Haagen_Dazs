# -*- coding: utf-8 -*-
{
    'name': 'POS Order Type',
    'summary': 'Allows you add Mode to POS orders',
    'version': '1.0',
    'description': """Allows you add Mode to POS orders""",
    'license': 'AGPL-3',
    'author': 'Fazal, Massab',
    'company': 'Fazal, Massab',
    'category': 'Point of Sale',
    'depends': [
        'base', 'point_of_sale',
    ],
    'external_dependencies': {'python': [],},
    'data': [
        'security/ir.model.access.csv',
        'views/pos_order_mode.xml',
        'views/posorder_view.xml',
        'views/templates.xml',
        ],
    'assets': {
        'point_of_sale.assets': [
            "pos_order_mode/static/src/js/db.js",
            "pos_order_mode/static/src/js/models.js",
            "pos_order_mode/static/src/js/PosOrderModeButton.js",
            "pos_order_mode/static/src/js/PosPayment.js",
        ],
        'web.assets_qweb': [
            'pos_order_mode/static/src/xml/PosOrderMode.xml'
        ],
     },
    'images': [],
    'installable': True
}
