# -*- coding: utf-8 -*-

from odoo import models, fields


class VLHREmployee(models.Model):
    _inherit = 'hr.employee'

    employee_number = fields.Char(string='Employee ID number', required=True)
    empass_equipement_ids = fields.One2many('maintenance.equipment', 'employee_id', string='Assigned equipment')


class VLHRDepartment(models.Model):
    _inherit = 'hr.department'

    dep_code = fields.Char(string="Department Code", required=True)
    depass_equipement_ids = fields.One2many('maintenance.equipment', 'department_id', string='Assigned equipment')
