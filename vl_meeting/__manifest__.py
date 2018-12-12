# -*- coding: utf-8 -*-

{
    'name': 'VL Meeting (Vedran Terihaj)',
    'version': '10.0.1.0.0',
    'category': 'Custom Lenac',
    'complexity': 'normal',
    'author': 'Vedran Terihaj',
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
