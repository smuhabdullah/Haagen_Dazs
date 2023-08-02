# -*- coding: utf-8 -*-

{
    "name": "POS Discount on Payment",
    "version": "1.6",
    "summary": "This module allows user to appy discount based on Payment method in Point of sale.| POS Promotion Selection",
    'description': """
POS Promtion Selection
==============================================
    =>Usually Default odoo doesn't provide a feature of payment method based discount in point of sale.
    """,
    'license': 'OPL-1',
    "category": "Sales/Point Of Sale",
    "website": "https://www",
    'author': 'Fazal, Massab',
    "depends": ['point_of_sale','pos_discount'],
    'data':[
        'data/default_data.xml',
        'views/pos_payment_method.xml',
        'views/pos_order.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            "pos_payment_disc/static/src/js/models.js",
            "pos_payment_disc/static/src/js/PaymentScreen.js",
        ],  
        'web.assets_qweb': [
            'pos_payment_disc/static/src/xml/PaymentMethodButton.xml',
        ],
     },
    "application": False,
    "installable": True,
}
