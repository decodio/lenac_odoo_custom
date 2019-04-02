{
    'name': "VL Palumbo exchange folders",
    'version': '10.0.0.1.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'maintainer': 'Viktor Lenac',
    'category': 'Tools',
    'website': '',
    'sequence': 1,
    'depends': ['cmis_field',
                'cmis_alf'],
    'installable': True,
    'auto_install': False,
    'qweb': [],

    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'views/vl_palumbo_exchange.xml',
             ],
    'description': """
                        This module is used to share data.
                    """,
}



