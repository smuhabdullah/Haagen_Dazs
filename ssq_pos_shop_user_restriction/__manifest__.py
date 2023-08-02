{
    "name": "POS Shop User Restriction",
    "summary": """Only allow access to selected POS shops for Odoo user""",
    "description": """
        In Odoo, a Point of Sale user will be able to view all the POS shops in the current company.
        This module will bring an Allowed POS Shops option in User form, where an administrator can
        restrict the access of the user to a limited number of POS shops. The user will be able to see
        all the POS shops if they are a Point of Sale Administrator.
    """,
    "author": "Sanesquare Technologies",
    "website": "https://www.sanesquare.com/",
    "support": "odoo@sanesquare.com",
    "license": "OPL-1",
    "category": "Sales/Point of Sale",
    "version": "15.0.1.0.1",
    "depends": ["point_of_sale"],
    "images": ["static/description/pos_shop_user_restriction_v15.png"],
    "data": [
        "security/security.xml",
        "views/res_users_view.xml",
    ],
}
