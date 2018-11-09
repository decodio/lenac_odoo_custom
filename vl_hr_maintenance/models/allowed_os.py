# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AllowedSoftware(models.Model):
    _name = 'allowed.os'

    sw_name = fields.Char(string="Software name")
    sw_vendor = fields.Char(string="Software vendor")
    sw_version = fields.Char(string="Software version")
    sw_licence = fields.Selection(selection=[('free', 'Free'), ('personal', 'Personal use'),
                                             ('spaid', 'Single paid licence'), ('mpaid', 'Multiple activation key')
                                             ],
                                  string='Licence type',
                                  required=False)
    sw_serial = fields.Char(string="Serial key")
    sw_purchase_date = fields.Date(string="Date of purchase")
    sw_licence_exp = fields.Date(string="Expiration date")
    sw_price = fields.Integer(string="Licence cost")
    sw_licence_assignd_person = fields.Many2one('hr.employee', string='Assigned to Employee')
    sw_licence_assignd_dep = fields.Many2one('hr.department', string='Assigned to Department')
    sw_spec = fields.Selection(selection=[('def', 'Installed by default'),
                                          ('dep_spec', 'Department specific')],
                               string='Installation type',
                               required='True')