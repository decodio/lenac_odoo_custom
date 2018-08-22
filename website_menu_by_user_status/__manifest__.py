{
    'name': 'Website Menu By User Display',
    'version': '8.0.1.1.0',
    'author': 'Savoir-faire Linux,Odoo Community Association (OCA)',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': 'Allow to manage the display of website.menus',
    'depends': [
        'website',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'views/website_templates.xml',
        'views/website_views.xml',
    ],
    'demo': [],
    'test': [],
    'installable': False,
}