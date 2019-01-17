# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from datetime import date, datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

#_LEAD_STATE = [
#    ('draft', 'New'),
#    ('open', 'In Progress'),
#    ('pending', 'Pending'),
#    ('done', 'Done'),
#    ('cancelled', 'Cancelled')]


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

    sort_of_equipment = fields.Selection([('production', 'Production Equipment'), ('ict', 'IT Equipment')],
                                         string='Sort of equipment',
                                         required=True,
                                         default='production')

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

    issue_ids = fields.One2many('project.issue', 'equipment_id', string='Issues',
                                domain=[('issue_type', '=', 'corrective')])

    issues_count = fields.Integer(compute='_compute_issues_count', string='Issues',
                                  store=True)

    """Ovaj dio koda ne radi;
    issues_open_count bi trebali vratiti vrijednost svih otvorenih issues ali ih ne prikazuju"""
    issues_open_count = fields.Integer(compute='_compute_issues_count', string="Current Issues", store=True)

    @api.one
    @api.depends('issue_ids')
    def _compute_issues_count(self):
        self.issues_count = len(self.issue_ids)
        self.issues_open_count = len(self.issue_ids.filtered(lambda x: x.state in ['draft', 'open', 'pending']))

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

    """SAME AS PREVENTIVE MAINTENANCE"""
    preventive_issue_ids = fields.One2many('project.issue', 'equipment_id', domain=[('issue_type', '=', 'preventive')])

    periods = fields.Integer('project.issue', related='preventive_issue_ids.period')

    next_action_dates = fields.Datetime('project.issue', related='preventive_issue_ids.next_action_date')

    @api.model
    def _create_new_issue(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'schedule_date': date,
            'category_id': self.category_id.id,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'user_id': self.technician_user_id.id,
        })

    @api.model
    def _cron_generate_issue(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for issue in self.search([('period', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state.done', '=', False),
                                                              ('equipment_id', '=', issue.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', issue.next_action_dates)])
            if not next_requests:
                issue._create_new_issue(issue.next_action_dates)


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
    _name = 'maintenance.request'
    _inherit = ['model.stage.control.common', 'maintenance.request']
    _stage_model_name = 'maintenance.stage'

    state = fields.Selection(
        related='stage_id.state', store=True, readonly=True)
    stage_sequence = fields.Integer(
        related='stage_id.sequence', store=True, readonly=True)

    equipment_project_code = fields.Char(string='Project code')
    equipment_project_type_id = fields.Many2one('vessel.project.type',
                                                string='Project Type(VP)')

    maintenance_child_equipment_ids = fields.One2many('maintenance.equipment',
                                                      related='equipment_id.child_equipment_ids',
                                                      readonly=True)

    child_equipment_issues = fields.One2many('project.issue', 'parent_equipment_id', string='Issues')

    issue_ids = fields.One2many('project.issue', 'parent_equipment_id', string='Issues')

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


class MaintenanceStage(models.Model):
    _name = 'maintenance.stage'
    _inherit = ['maintenance.stage', 'stage.control.common']

#    state = fields.Selection(_LEAD_STATE, 'State')
    create_code = fields.Boolean(string='Create Code')


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    issues_count = fields.Integer(string="Issues", compute='_compute_issues_count')

    @api.multi
    def _compute_issues_count(self):
        issues_data = self.env['project.issue'].read_group([('category_id', 'in', self.ids)],
                                                           ['category_id'], ['category_id'])
        mapped_data = dict([(m['category_id'][0], m['category_id_count']) for m in issues_data])
        for category in self:
            category.issues_count = mapped_data.get(category.id, 0)


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    equipment_id = fields.Many2one('maintenance.equipment',
                                   string='Equipment',
                                   index=True,
                                   track_visibility='onchange'
                                   )

    category_id = fields.Many2one('maintenance.equipment.category', related='equipment_id.category_id',
                                  string='Category', store=True, readonly=True)

    parent_equipment_id = fields.Many2one('maintenance.equipment', compute='_compute_parent_equipment_id',
                                          string="Parent equipment", store=True, readonly=True)

    @api.depends('equipment_id')
    def _compute_parent_equipment_id(self):
        for issue in self:
            if issue.equipment_id:
                issue.parent_equipment_id = issue.equipment_id.parent_equipment_ids
            else:
                issue.parent_equipment_id = False

    """zapisuje se parent project code kako bi se prema njemu mogli dohvatiti svi Issues na formu maintenance request"""
#    maintenance_request_ids = fields.Many2one('maintenance.request',
#                                             related='equipment_id.equipment_project_code')

    schedule_date = fields.Datetime('Scheduled Date')

    issue_type = fields.Selection([('corrective', 'Corrective'),
                                   ('preventive', 'Preventive')],
                                  string='Issue Type',
                                  default="corrective")

#   date = request_date = fields.Date('Request Date', track_visibility='onchange', default=fields.Date.context_today,
#                                     help="Date requested for the issue to happen")
#   date_done_iss = close_date = fields.Date('Close Date', help="Date the issue was finished. ")

    item_specification = fields.Char('Specification item')

    period = fields.Integer('Days between each preventive issue')

    next_action_date = fields.Datetime(compute='_compute_next_issue',
                                       string='Date of the next preventive issue', store=True)

    @api.depends('period', 'date', 'date_done_iss')
    def _compute_next_issue(self):

        date_now = fields.Date.context_today(self)
        for issue in self.filtered(lambda x: x.period > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', issue.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done')])
#                ('close_date', '=', False)], order="request_date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', issue.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done')])
#                ('close_date', '!=', False)], order="close_date desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(days=issue.period) * 2 and fields.Date.from_string\
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=issue.period) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=issue.period))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=issue.period) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=issue.period))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(days=issue.period)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(fields.Date.from_string(date_now) + timedelta(days=issue.period))

            issue.next_action_date = next_date


