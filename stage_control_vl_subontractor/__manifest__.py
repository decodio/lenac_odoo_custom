# -*- coding: utf-8 -*-
# Copyright © 2017 Decodio d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name' : 'Stage Control VL Subcontractor',
    'version' : '10.0.1.0.0',
    'sequence': 100,
    'category': 'Tools',
    'complexity': "normal",
    'author': 'Decodio d.o.o. - Goran Kliska, Dario Meniss',
    'website': '',
    'description': """
Stage Control VL Subcontractor
===============================


Main Features
-------------
* required fields per stage
* automatic tasks per stage
* email-template per stage

""",
    'depends': [
        'sp_viktor_lenac_dms_qms',
        'stage_control_base',
        'vl_subcontractor',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/vl_subcontractor_stage.xml',
        'views/vl_subcontractor_stage_view.xml',
        'views/vl_subcontractor_view.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
