# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Viktor Lenac (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac/VL B2B Theme',
    'complexity': "normal",
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'http://lenac.hr',
    'depends': ['website'],
    'data': [
        'views/layout.xml',
        'views/pages.xml',
        'views/assets.xml',
        'views/snippets.xml',
        #'data/vl_custom_data.xml',
    ],
    'summary': 'Tema za B2B portal',
    'description': '',
    'category': 'Theme',
    'sequence': 900,
    'images': ['/vl_theme/static/src/img/ui/snippet_thumb.png'],
    'application': False,
}
