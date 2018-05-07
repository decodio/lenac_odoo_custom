# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'HR Subcontractor',
    'version': '10.0.1.0.0',
    'category': 'Custom/Lenac',
    'complexity': "normal",
    'author': 'OpenERP SA custom (Vedran Terihaj)',
    'website': 'http://lenac.hr',
    'depends': ['sp_viktor_lenac_dms_qms',
                'hr',
                'calendar',
                'survey',],  # List dependent modules, sp_viktor_lenac_dms_qms is a safe bet
    'data': [
             #'security/ir.model.access.csv',
             #'security/website_vl_subcontractor_security.xml',
             #'views/vl_subcontractor_view.xml',
             'views/vl_hr_evaluation_view.xml',
             'data/vl_hr_evaluation_data.xml',
             'data/vl_hr_evaluation_installer.xml',
             'data/vl_survey_data_appraisal.xml',
             ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'images': [],
    'description': '''Evaluation of subcontractor workforce, specific to VL modified modul hr_evaluation''',
}
