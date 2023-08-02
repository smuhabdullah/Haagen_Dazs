# -*- coding: utf-8 -*-
{
    'name': "Cash Bank In Out Report",
    'summary': """ """,
    'description': """ """,
    'author': "My Company",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','account'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/cash_report_wizard.xml',
        'report/report.xml',
        'report/report_cash_in_out.xml',
    ],
}
