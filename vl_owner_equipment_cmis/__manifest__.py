# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CMIS VL Owner equipment (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['vl_owner_equipment',
                'cmis_field',
                'cmis_alf'],
    'data': ['data/owner_equipment.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'description': """
        Document tab for tracking equipment removed from projects""",
    'summary': '',
}
