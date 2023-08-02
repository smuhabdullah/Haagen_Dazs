# -*- coding: utf-8 -*-

{
    "name": "POS Session Opening Stock",
    "version": "1.1",
    "summary": "This module allows user to set opening stock for specified product in Point of sale Opening session.",
    'description': """
POS Coupon Selection
==============================================
    =>Usually Default odoo doesn't provide a feature of opening stock for session in point of sale.
    => This module allow you to set opening stock for products, the when the user close the session, the session closing stock will be entered
    """,
    'license': 'OPL-1',
    "category": "Sales/Point Of Sale",
    "website": "https://www",
    'author': 'Fazal, Massab',
    "depends": ['point_of_sale'],
    'data':[
        'security/ir.model.access.csv',
        'views/pos_session.xml',
        'views/product.xml',
        'wizards/session_stock_wizard.xml',
        'views/pos_config.xml',
    ],
    "application": False,
    "installable": True,
}
