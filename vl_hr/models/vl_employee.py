# -*- coding: utf-8 -*-

from odoo import models, fields


class VLHREmployee(models.Model):
    _inherit = 'hr.employee'

    employee_number = fields.Char(string='Employee ID number')
