# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Edu report 2',
    'version': '10.0.0.0.0',
    'category': 'Custom/Lenac',
    'complexity': "normal",
    'author': 'Viktor Lenac',
    'website': 'http://lenac.hr',
    'depends': ['sp_viktor_lenac_dms_qms'],  # List dependent modules, sp_viktor_lenac_dms_qms is a safe bet
    'data': [
             'security/ir.model.access.csv',
             'views/lead_report1_view.xml',
             ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'images': [],
    'description': '''Example report. Template for new report''',
}
