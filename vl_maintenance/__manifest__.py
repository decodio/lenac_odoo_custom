# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Equipments (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['hr',
                'hr_maintenance',
                'vl_hr',
                'sp_viktor_lenac',
                'sp_viktor_lenac_dms_qms',
                'project_issue',
                'stage_control_base',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/vl_maintenance_cron.xml',
        'report/report.xml',
        'report/personal_equipment.xml',
        'views/vl_maintenance_views.xml',
        'views/allowed_os.xml',
        'views/hardware.xml',
        'views/network_resources.xml',
        'views/ad_groups.xml',
        'views/database.xml',
        'views/application.xml'
    ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """
        Adds software and hardware inventory + licence tracking for Shipyard Viktor Lenac""",
    'summary': 'ICT Inventory tracking',
}
