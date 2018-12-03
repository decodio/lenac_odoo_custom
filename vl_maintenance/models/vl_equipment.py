# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

import logging
_logger = logging.getLogger(__name__)


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('report.external_layout')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('report.external_layout', docargs)

    pc_number = fields.Char('Inventory number')
    """ OLD
    installed_os = fields.Selection(
      selection=[('winxp', 'Windows XP'), ('win7', 'Windows 7'), ('win10', 'Windows 10'),
                 ('winser2003', 'Windows Server 2003'), ('winser2008', 'Windows Server 2008'),
                 ('winser2008R2', 'Windows Server 2008 R2'), ('winser2012', 'Windows Server 2012'),
                 ('winser2012R2', 'Windows Server 2012 R2')],
      string='Installed OS',
      required=False)
    """
    installed_os = fields.Many2one('maintenance.allowed.os', string='Installed OS')
    installed_sw = fields.Many2many('maintenance.allowed.os', string='Installed software')
    date_purchased = fields.Date('Date of purchase')

    new_employee_number = fields.Char('hr.employee',
#                                      string='Assigned employee number',
                                      related='employee_id.employee_number',
                                      readonly=True,
                                      store=True)

    new_department_number = fields.Char('hr.department',
#                                       string='Assigned department number',
                                        related='department_id.department_code',
                                        readonly=True,
                                        store=True)

    old_equipment_assign_to = fields.Selection([('department', 'Department'),
                                                ('employee', 'Employee'),
                                                ('other', 'Other')],
                                               string='Used By',
                                               required=True,
                                               default='employee')

    old_employee_id = fields.Many2one('hr.employee', string='Assigned to Employee', track_visibility='onchange')

    old_department_id = fields.Many2one('hr.department', string='Assigned to Department', track_visibility='onchange')

    old_employee_number = fields.Char('hr.employee',
#                                     string='Employee number',
                                      related='old_employee_id.employee_number',
                                      readonly=True,
                                      store=True)

    old_department_number = fields.Char('hr.department',
#                                       string='Department number',
                                        related='old_department_id.department_code',
                                        readonly=True,
                                        store=True)

    date_assigned = fields.Date('Date assigned')
    new_location = fields.Char('Assigned location')
    components = fields.One2many('maintenance.hardware.details', 'installed_on_pc',
                                 string='Installed Components')

    sort_of_equipment = fields.Selection([('production', 'Production Equipment'), ('ict', 'IT Equipment')],
                                         string='Sort of equipment',
                                         required=True,
                                         default='production')

    child_equipment_ids = fields.One2many('maintenance.equipment', 'parent_equipment_ids',
                                          string='Child equipment',
                                          readonly=True)

    parent_equipment_ids = fields.Many2one('maintenance.equipment',
                                           string='Parent equipment',
                                           readonly=False,
                                           store=True)



    @api.multi
    def create_new_issue(self):
        # issue_id = self.issue_id
        view_ref = self.env['ir.model.data'].get_object_reference('sp_viktor_lenac', 'project_issue_lenac_form_view')
        view_id = view_ref[1] if view_ref else False
        res = {
            "type": "ir.actions.act_window",
            "res_model": "project.issue",
            "view_type": "form",
            "view_mode": "form",
            "view_id": view_id,
            "target": "new",
            "context": {}

        }
        return res

    issue_ids = fields.One2many('project.issue', 'equipment_id')

    issues_count = fields.Integer(compute='_compute_issues_count', string="Issues",
                                  store=True)

    issues_open_count = fields.Integer(compute='_compute_issues_count', string="Current Issues",
                                       store=True)

    @api.one
    @api.depends('issue_ids')
    def _compute_issues_count(self):
        self.issues_count = len(self.issue_ids)
        self.issues_open_count = len(self.issue_ids.filtered(lambda x: not x.state.done))


"""
    issues_count = fields.Integer(string="Issues",
                                  store=True,
                                  compute='_compute_issues_count'
                                  )
    @api.one
    @api.depends('issues_ids.state.done')
    def _compute_issues_count(self):
        self.issues_count = len(self.issues_ids)
        self.issues_open_count = len(self.issues_ids.filtered(lambda x: not x.state.done))
    """
"""
    @api.multi
    def raise_new_issue(self):
        return({
            "type": "ir.actions.act_window",
            "res_model": "project.issue",
            "view_type": "form",
            "view_mode": "form",
            "views": [[False, "form"]],
            "target": "new"
            })
    """
"""
     def show_ru_assignments_sub_view(self, cr, uid, ids, context=None):
        return {
               'name': ('Assignment Sub'),
               'view_type': 'form',
               'view_mode': 'form',
               'res_model': 'ru.assignments.sub',
               'view_id': False,
               'type': 'ir.actions.act_window',
               'target': 'new'
               }

    model_A1 = fields.Char()
    model_desc = fields.Char()
    model_A1_child = fields.Many2one('modelA')
    model_A1_desc = fields.Char(related='model_A1_child.model_desc')

    @api.depends('employee_id')
    def _compute_emp_number(self):
        for equipment in self:
            if equipment.employee_id:
                equipment.new_employee_number = equipment.employee_id[:1].employee_number
            else:
                equipment.new_employee_number = False

    @api.depends('old_employee_id')
    def _compute_old_emp_number(self):
        for equipment in self:
           if equipment.old_employee_id:
                equipment.old_employee_number = equipment.old_employee_id[:1].employee_number
            else:
                equipment.old_employee_number = False

    @api.depends('department_id')
    def _compute_dep_number(self):
        for equipment in self:
            if equipment.department_id:
                equipment.new_department_number = equipment.department_id[:1].department_code
            else:
                equipment.new_department_number = False

    @api.depends('old_department_id')
    def _compute_old_dep_number(self):
        for equipment in self:
            if equipment.old_department_id:
                equipment.old_department_number = equipment.old_department_id[:1].department_code
            else:
                equipment.old_department_number = False
"""


class MaintenanceAllowedOs(models.Model):
    _name = 'maintenance.allowed.os'
    _description = 'Installed software'

    name = fields.Char(string="Software name", required='True')
    sw_vendor = fields.Char(string="Software vendor")
    sw_version = fields.Char(string="Software version")
    sw_licence = fields.Selection(selection=[('free', 'Free'), ('personal', 'Personal use'),
                                             ('spaid', 'Single paid licence'), ('mpaid', 'Multiple activation key'),
                                             ('subs', 'Subscription')],
                                  string='Licence type',
                                  required=False)
    sw_serial = fields.Char(string="Serial key")
    sw_purchase_date = fields.Date(string="Date of purchase")
    sw_licence_exp = fields.Date(string="Expiration date")
    sw_price = fields.Integer(string="Licence cost")
    sw_licence_assigned_person = fields.Many2one('hr.employee', string='Assigned to Employee')
    sw_licence_assigned_dep = fields.Many2one('hr.department', string='Assigned to Department')
    sw_spec = fields.Selection(selection=[('def', 'Installed by default'),
                                          ('dep_spec', 'Department specific')],
                               string='Installation type',
                               required='True')
    sw_type = fields.Selection(selection=[('prog', 'Program'), ('OS', 'Operating system')],
                               string='Software type',
                               required='True')


class MaintenanceHardwareDetails(models.Model):
        _name = 'maintenance.hardware.details'
        _description = 'Hardware Details'

        name = fields.Char(string='Component name')
        manufacturer = fields.Char(string='Manufacturer')
        serial_no = fields.Char(string='Serial Number')
        component_type = fields.Many2one('maintenance.component.type', string='Component type')
        size = fields.Char(string='Size')
        status = fields.Selection(selection=[('inst', 'Installed'), ('rep', 'Replaced'), ('war', 'Warranty')],
                                  string='Component status',
                                  required='True')
        log_note = fields.Text(string='Log of internal notes')
        purchase_date = fields.Date(string='Date of purchase')
        warranty = fields.Char(string='Warranty')
        warranty_valid = fields.Date(string='Warranty till')
        price = fields.Char(string='Cost')
        installed_on_pc = fields.Many2one('maintenance.equipment',
                                          realted='name',
                                          track_visibility='onchange',
                                          readonly=False)


class MaintenanceComponentType(models.Model):
        _name = 'maintenance.component.type'

        name = fields.Char(string='Component type')


class MaintenanceRequest(models.Model):
    _inherit = ['maintenance.request']

    equipment_project_code = fields.Char(string='Project code')
    equipment_project_type = fields.Many2one('vessel.project.type',
                                             string='Project Type(VP)')

    maintenance_child_equipment_ids = fields.One2many('maintenance.equipment', 'child_equipment_ids',
                                                      readonly=True)


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    equipment_id = fields.Many2one('maintenance.equipment',
                                   realted='name',
                                   string='Equipment',
                                   track_visibility='onchange',
                                   readonly=False
                                   )



"""
class HREmployeeEq(models.Model):
    _inherit = 'hr.employee'

    empass_equipement_ids = fields.One2many('maintenance.equipment', 'employee_id', string='Assigned equipment')


class HRDepartmentEq(models.Model):
    _inherit = 'hr.department'

    depass_equipement_ids = fields.One2many('maintenance.equipment', 'department_id', string='Assigned equipment')
"""