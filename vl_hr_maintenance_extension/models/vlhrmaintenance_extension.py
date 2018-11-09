# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class VLHRMaintenanceExtension(models.Model):

    _description = 'VL HR Maintenance extension'
    _inherit = 'maintenance.equipment'

    inventory_number = fields.Integer('Inventory number')
    installed_os = fields.Selection(
        selection=[('winxp', 'Windows XP'), ('win7', 'Windows 7'), ('win10', 'Windows 10'),
                   ('winser2003', 'Windows Server 2003'), ('winser2008', 'Windows Server 2008'),
                   ('winser2008R2', 'Windows Server 2008 R2'), ('winser2012', 'Windows Server 2012'),
                   ('winser2012R2', 'Windows Server 2012 R2')],
        string='Installed OS',
        required=False)
    installed_sw = fields.Many2many('allowed_software', string='Installed software')
