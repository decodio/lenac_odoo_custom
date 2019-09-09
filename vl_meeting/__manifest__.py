# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'VL Meeting (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Viktor Lenac d.d. (Vedran Terihaj)',
    'website': 'https://lenac.hr',
    'license': '',
    'depends': [
                'calendar',
                ],
    'data': [
            'data/vl_mail_template.xml',
            'report/report.xml',
            'report/meeting_report.xml',
            'views/vl_meeting.xml',
            ],
    'demo': [],
    'installable': True,
    'auto-install': False,
    'description': """
        Extension of the meeting form with meeting report witch can be sent by e-mail to all participants for 
        Shipyard Viktor Lenac""",
    'summary': 'Meeting summary',
}
