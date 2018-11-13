# -*- coding: utf-8 -*-

{
    'name': 'VL Equipments (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': ['hr',
                'maintenance',
                'hr_maintenance',
                ],
    'data': [
            'security/equipment.xml',
            'report/report.xml',
            'report/personal_equipment.xml',
            'views/vl_maintenance_views.xml',
            'views/allowed_os.xml',
            'views/hardware.xml',
            ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """
        Adds software inventory and licence tracking for Shipyard Viktor Lenac""",
    'summary': 'ICT Inventory tracking',
}
