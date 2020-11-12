# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL MGMTSYSTEM MULTI (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['mgmtsystem_audit',
                'mgmtsystem_requirement',
                'sp_viktor_lenac',
                'sp_viktor_lenac_dms_qms',
                ],
    'data': [
        'views/vl_mgmt_system_audit.xml',
    ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """
        Adds multi system for audits and verification line for Shipyard Viktor Lenac""",
    'summary': 'Audit multi system',
}
