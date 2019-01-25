# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_number = fields.Char(string='Employee ID number', required=True)

    # empass_equipement_ids = fields.Many2one('maintenance.equipment', 'employee_id', string='Assigned equipment')
    employee_assigned_equipment_ids = fields.One2many('maintenance.equipment', 'employee_id'
                                                      #string='Assigned equipment'
                                                      )

    work_phone_short = fields.Char('Work Phone Short')
    mobile_phone_short = fields.Char('Work Mobile Short')


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    department_code = fields.Char(string="Department Code", required=True)

    department_assigned_equipment_ids = fields.One2many('maintenance.equipment', 'department_id'
                                                        #string='Assigned equipment'
                                                        )

    employee_id = fields.One2many('hr.employee', 'department_id')

