# -*- coding: utf-8 -*-

{
    'name': 'VL Equipments (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'http://lenac.hr',
    'depends': ['hr',
                'maintenance',
                'hr_maintenance', ],
    'data': [
            'views/vl_maintenance_views.xml',
            'views/allowed_os.xml',
            ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """
        Adds software inventory and licence tracking""",
    'summary': 'Equipments, Assets, Internal Hardware, Allocation Tracking',
}
