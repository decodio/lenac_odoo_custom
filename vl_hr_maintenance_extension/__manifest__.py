# -*- coding: utf-8 -*-

{
    'name': 'VL HR - Equipments',
    'version': '1.0',
    'sequence': 125,
    'description': """
        Bridge between HR and Maintenance.""",
    'depends': ['hr', 'maintenance', 'hr_maintenance'],
    'summary': 'Extends the from for VL ICT inventory tracking',
    'data': [
        'security/equipment.xml',
        'views/maintenance_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto-install': True,
}
