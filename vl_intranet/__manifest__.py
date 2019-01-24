# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Intranet (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': "Viktor Lenac d.d. (Vedran Terihaj)",
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['website_portal',],
    'data': [
        'views/website_intranet_views.xml',
        'views/vl_news_articles.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'description': """
        Shipyard Viktor Lenac intranet portal for registered users""",
    'summary': 'Viktor Lenac intranet',
}
