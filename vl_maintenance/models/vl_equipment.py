# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

_LEAD_STATE = [
    ('draft', 'New'),
    ('open', 'In Progress'),
    ('pending', 'Pending'),
    ('done', 'Done'),
    ('cancelled', 'Cancelled')]


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
    installed_os = fields.Many2one('maintenance.allowed.os', string='Installed OS')
    installed_sw = fields.Many2many('maintenance.allowed.os', string='Installed software')
    date_purchased = fields.Date('Date of purchase')

    new_employee_number = fields.Char('hr.employee',
                                      related='employee_id.employee_number',
                                      readonly=True,
                                      store=True)

    new_department_number = fields.Char('hr.department',
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
                                      related='old_employee_id.employee_number',
                                      readonly=True,
                                      store=True)

    old_department_number = fields.Char('hr.department',
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

    parent_equipment_ids = fields.Many2one('maintenance.equipment',
                                           string='Parent equipment',
                                           readonly=False,
                                           store=True)

    child_equipment_ids = fields.One2many('maintenance.equipment', 'parent_equipment_ids',
                                          string='Child equipment',
                                          readonly=True)

#    project_code = fields.Many2one('maintenance.request', 'equipment_project_code')
#    @api.multi
#    def name_get(self):
#        result = []
#        for record in self:
#            project_code = record.project_code
#            if record.parent_equipment_ids:
#                project_code = "%s / %s" % (record.parent_equipment_ids.name_get()[0][1], project_code)
#            result.append((record.id, project_code))
#        return result

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

    """Ovaj dio koda ne radi; 
     
    issues_count bi trebao vratiti broj svih issues za taj equipmnet
     
    issues_open_count bi trebali vratiti vrijednost svih otvorenih issues ali ih ne prikazuju"""

    issue_ids = fields.One2many('project.issue', 'equipment_id', string='Issues')

    issues_count = fields.Integer(compute='_compute_issues_count', string='Issues',
                                  store=True)

    issues_open_count = fields.Integer(compute='_compute_issues_count', string="Current Issues", store=True)

    @api.one
    @api.depends('issue_ids')
    def _compute_issues_count(self):
        self.issues_count = len(self.issue_ids)
        self.issues_open_count = len(self.issue_ids.filtered(lambda x: not x.state.done))

    employee_department_new = fields.Many2one('hr.department',
                                              compute='_compute_new_department_id',
                                              readonly=True,
                                              store=True)
    employee_department_old = fields.Many2one('hr.department',
                                              compute='_compute_old_department_id',
                                              readonly=True,
                                              store=True)
    employee_department_new_number = fields.Char('hr.department',
                                                 related='employee_department_new.department_code',
                                                 readonly=True,
                                                 store=True)
    employee_department_old_number = fields.Char('hr.department',
                                                 related='employee_department_old.department_code',
                                                 readonly=True,
                                                 store=True)

    @api.depends('employee_id')
    def _compute_new_department_id(self):
        for equipment in self:
            if equipment.employee_id:
                equipment.employee_department_new = equipment.employee_id.department_id
            else:
                equipment.employee_department_new = False

    @api.depends('old_employee_id')
    def _compute_old_department_id(self):
        for equipment in self:
            if equipment.old_employee_id:
                equipment.employee_department_old = equipment.old_employee_id.department_id
            else:
                equipment.employee_department_old = False


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
    equipment_project_type_id = fields.Many2one('vessel.project.type',
                                                string='Project Type(VP)')

    maintenance_child_equipment_ids = fields.One2many('maintenance.equipment',
                                                      related='equipment_id.child_equipment_ids',
                                                      readonly=True)

    @api.multi
    def write(self, vals=None):
        # CREATE PROJECT CODE (sequence defined on vessel_project_type_id)
        if (vals.get('stage_id') and
                vals.get('vessel_project_type_id', self.equipment_project_type_id) and
                (not self.equipment_project_code)):
            if self.env['maintenance.stage'].browse(vals['stage_id']).create_code:
                seq = self.equipment_project_type_id.sequence_id and \
                      self.equipment_project_type_id.sequence_id.next_by_id() or ''
                current_year = str(datetime.now().year)
                equipment_project_code = (current_year[2:] + str(self.equipment_project_type_id.code or '') + seq)
                if seq:
                    vals.update({'equipment_project_code': equipment_project_code})

        res = super(MaintenanceRequest, self).write(vals)
        return res

#    maintenance_child_equipment_issue_id = fields.One2many(
#        'project.issue',
#        related='maintenance_request_ids',
#        readonly=True)


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    """Nije moguće dodati equipment na issue"""
    equipment_id = fields.Many2one('maintenance.equipment',
                                   string='Equipment',
                                   index=True,
                                   track_visibility='onchange'
                                   )

    """zapisuje se parent project code kako bi se prema njemu mogli dohvatiti svi Issues na formu maintenance request"""
#    maintenance_request_ids = fields.Many2one('maintenance.request',
#                                             related='equipment_id.equipment_project_code')


class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    #state = fields.Selection(_LEAD_STATE, 'State')
    create_code = fields.Boolean(string='Create Code')
