# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Energy (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['sp_viktor_lenac',
                'sp_viktor_lenac_dms_qms',
                ],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/vl_energy.xml',

            ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """
        Energy tracking by project""",
    'summary': 'Energy tracking on projects',
}
