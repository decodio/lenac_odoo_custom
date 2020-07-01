# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Job Long Stage control(Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['hr',
                'vl_hr',
                'stage_control_base',
                ],
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        # 'views/vlhr_employee.xml',
        # 'views/website_vlhr_employee_views.xml',
        # 'report/report.xml',
        # 'report/job_description_department.xml',
        # 'report/job_risk.xml',
        # 'report/job_description.xml',
        # 'wizard/hr_job_approval_reject_reason_wizard_view.xml',
        'views/hr_job_stage_view.xml',
        'views/hr_job_view.xml',
        'views/hr_job_stage_approval_view.xml',
        'views/hr_job_approval_history_view.xml',
        # 'views/document_page_read_history_view.xml',
        'wizard/hr_job_approval_reject_reason_wizard_view.xml'
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'description': """
        Extends the module for Shipyard Viktor Lenac""",
    'summary': 'ICT Inventory tracking',
}
