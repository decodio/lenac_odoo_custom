# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Owner equipment (Vedran Terihaj)',
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
            'report/vl_owner_equipment.xml',
            'report/vl_owner_equipment_container.xml',
            'report/report.xml',
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/owner_equipment_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'description': """
        Tracking equipment removed from projects""",
    'summary': '',
}
