# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Reports (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Vedran Terihaj',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['mgmtsystem_audit',
                'mgmtsystem_requirement',
                'mgmtsystem_nonconformity',
                'sp_viktor_lenac',

                ],
    'data': [
            'report/audit_plan.xml',
            'report/audit_report.xml',
            'report/ncr_report.xml',
            'report/report.xml',
            'report/verification_list.xml',
            ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """Reports module for Shipyard Viktor Lenac""",
    'summary': 'VL Reports',
}
