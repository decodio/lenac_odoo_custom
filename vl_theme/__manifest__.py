# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Viktor Lenac (Vedran Terihaj)',
    'summary': 'Tema za B2B portal',
    'description': '',
    'category': 'Theme',
    'sequence': 900,
    'version': '1.0',
    'author': 'Vedran Terihaj',
    'depends': ['website'],
    'data': [
        #'data/theme_bootswatch_data.xml',
        'views/layout.xml',
        'views/pages.xml',
        'views/assets.xml',
    ],
    'images': ['static/description/bootswatch.png'],
    'application': False,
}
