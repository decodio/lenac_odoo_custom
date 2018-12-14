{
    'name': "CMIS tab on Maintenance",
    'version': '10.0.0.1.0',
    'maintainer': 'Decodio Aplications',
    'category': 'Tools',
    'website': '',
    'sequence': 1,
    'description': """

 License: MIT
    Uninstall this module
    """,
    'installable': True,
    'auto_install': True,
    'qweb': [],
    'depends': ['vl_maintenance',
                'cmis_field',
                'cmis_alf'],
    'data': ['data/maitenance_equipment.xml',
             ],

}
