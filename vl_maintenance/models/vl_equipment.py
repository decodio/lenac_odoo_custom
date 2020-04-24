# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)


#    _LEAD_STATE = [
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

    sort_of_equipment = fields.Selection([('production', 'Production Equipment'),
                                          ('ict', 'IT Equipment'),
                                          ('sm_production', 'Small equipment')],
                                         string='Sort of equipment',
                                         required=True,
                                         default='production')

    pc_number = fields.Char('Inventory number')
    barcode_number = fields.Char('Barcode')
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

    network_resources = fields.Many2many('maintenance.network.resources')
    location_name = fields.Char(string="Location name")

    preventive_maintenance_ids = fields.One2many(
        'maintenance.issue.plan',
        'equipment_id')

    """SAME AS PREVENTIVE MAINTENANCE"""
    preventive_issue_ids = fields.One2many(
        'project.issue',
        'equipment_id',
        domain=[('issue_type', '=', 'preventive')])

    next_action_dates = fields.Datetime(
        string='Date of the next preventive issue', readonly=True, store=True,
        track_visibility='onchange')

    inventoried = fields.Boolean(string='Inventoried', help='If checked Yes')

    no_of_pieces = fields.Integer(string='Number of pieces', default='1')

    """SMALL EQUIPMENT"""

    equipment_tracking_ids = fields.One2many('maintenance.equipment.tracking',
                                             'sm_equipment_id',
                                             track_visibility='always')

    number_of_pieces = fields.Integer(compute='_compute_equipment',
                                      string="Current Number of Equipment",
                                      help='Current number of equipment',
                                      readonly=False)

    number_of_piecese = fields.Integer(compute='_compute_equipment',
                                       string="Current Number of Equipment used",
                                       store=True,
                                       help='Current number of equipment used')

    number_of_piecesst = fields.Integer(compute='_compute_equipment',
                                        string="Current Number of Equipment in Storage",
                                        store=True,
                                        help='Current number of equipment in storage')

    @api.depends('equipment_tracking_ids.sm_equipment_id',
                 'equipment_tracking_ids.sm_equipment_assign_to')
    def _compute_equipment(self):
        equipment_data = self.env['maintenance.equipment.tracking'].read_group(
            [('sm_equipment_id', 'in', self.ids)], ['sm_equipment_id'],
            ['sm_equipment_id'])
        result = dict(
            (data['sm_equipment_id'][0], data['sm_equipment_id_count']) for data
            in
            equipment_data)

        equipment_data_ae = self.env[
            'maintenance.equipment.tracking'].read_group(
            [('sm_equipment_id', 'in', self.ids),
             ('sm_equipment_assign_to', '=', 'employee')],
            ['sm_equipment_id'], ['sm_equipment_id'])
        result_ae = dict(
            (data['sm_equipment_id'][0], data['sm_equipment_id_count']) for data
            in
            equipment_data_ae)

        equipment_data_st = self.env[
            'maintenance.equipment.tracking'].read_group(
            [('sm_equipment_id', 'in', self.ids),
             ('sm_equipment_assign_to', '=', 'other')], ['sm_equipment_id'],
            ['sm_equipment_id'])
        result_st = dict(
            (data['sm_equipment_id'][0], data['sm_equipment_id_count']) for data
            in
            equipment_data_st)

        for equipment in self:
            equipment.number_of_piecesst = result_st.get(equipment.id, 0)
            equipment.number_of_piecese = result_ae.get(equipment.id, 0)
            equipment.number_of_pieces = result.get(equipment.id, 0)


class MaintenanceAllowedOs(models.Model):
    _name = 'maintenance.allowed.os'
    _description = 'Installed software'

    name = fields.Char(string="Software name", required='True')
    sw_inventory_number = fields.Char(string="Inventory number")
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
    sw_related = fields.One2many('maintenance.application', 'application_select')


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

    issue_type = fields.Selection([('corrective', 'Corrective'),
                                   ('preventive', 'Preventive')],
                                  string='Issue Type',
                                  default="corrective")

    schedule_date = fields.Datetime('Scheduled Date')

    item_specification = fields.Char('Specification item')

    next_action_date = fields.Datetime('maintenance.equipment', related='equipment_id.next_action_dates')

    related_module_menu = fields.One2many('maintenance.menu.view', 'related_issue')

    maintenance_issue_plan_id = fields.Many2one(
        'maintenance.issue.plan',
        string='MaintenancePlan')


class MaintenancePlan(models.Model):
    _name = 'maintenance.issue.plan'

    name = fields.Char("Maintenance issue name")
    period = fields.Integer('Period of maintenance (In Days)')

    next_action_date = fields.Datetime(
        string='Date of the next preventive issue',
    )
    description = fields.Text('Describe the next maintenance')
    project_id = fields.Many2one(
        'project.project',
         string='Select issue type',
         store='True')
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipment',
        index=True)

    @api.model
    def create(self, vals):
        res = super(MaintenancePlan, self).create(vals)
        res.create_new_issue(fields.Date.context_today(res))
        return res

    @api.onchange('period')
    def _onchange_period(self):
        date_now = fields.Date.from_string(fields.Date.today())
        next_date = date_now + relativedelta(days=self.period)
        self.next_action_date = next_date

    @api.multi
    def create_new_issue(self, date):
        self.ensure_one()
        issue = self.env['project.issue'].with_context(without_dms=True).create({
                'name': _('Preventive issue - %s') % self.name,
                'date': date,
                'equipment_id': self.equipment_id.id,
                'project_id': self.project_id.id,
                'issue_type': 'preventive',
                'description': self.description,
                'schedule_date': date,
                'issuer_id': self.env.uid,
                'maintenance_issue_plan_id': self.id,
            })
        return issue

    @api.model
    def _cron_generate_issue(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        today_start = fields.Datetime.from_string(fields.Date.today())
        today_end = today_start + relativedelta(days=1)
        maintenance_plan_ids = self.search([
            ('period', '>', 0),
            ('next_action_date', '>=', fields.Datetime.to_string(today_start)),
            ('next_action_date', '<', fields.Datetime.to_string(today_end)),
            ])
        for maintenance_plan in maintenance_plan_ids:
            issue = maintenance_plan.create_new_issue(
                maintenance_plan.next_action_date)
            if issue:
                next_date = fields.Date.from_string(
                    maintenance_plan.next_action_date) +\
                            relativedelta(days=maintenance_plan.period)
                maintenance_plan.write({'next_action_date': next_date})


class MaintenanceNetworkResources(models.Model):
    _name = 'maintenance.network.resources'
    _description = 'Shared network resources'

    name = fields.Char(string='Resource name')
    parent_equipment_id = fields.Many2many('maintenance.equipment')
    user_groups = fields.Many2many('maintenance.ad.groups', string='Allowed AD Groups')
    # allowed_users = fields.Many2many('maintenance.ad.groups', related='allowed_users', string='Allowed AD users')


class MaintenanceADGroups(models.Model):
    _name = 'maintenance.ad.groups'
    _description = 'AD user groups'

    name = fields.Char(string='AD User group')
    allowed_users = fields.Many2many('hr.employee', string='AD Users')


class MaintenanceApplication(models.Model):
    _name = 'maintenance.application'
    _description = 'Applications used in VL'

    name = fields.Char(string='Application name')
    application_select = fields.Many2one('maintenance.allowed.os', domain=[('sw_type', '=', 'prog')])
    application_module = fields.One2many('maintenance.module.items', 'application')
    application_master_project = fields.Many2one('project.project')
    a_related_hours = fields.Float(compute='_a_compute_sum_hours_spent',
                                   readonly=True,
                                   track_visibility='onchange')
    a_related_cost_cooperation = fields.Float(compute='_a_compute_sum_cost_cooperation',
                                              readonly=True,
                                              track_visibility='onchange')

    @api.multi
    def _a_compute_sum_hours_spent(self):
        for rec in self:
            rec.a_related_hours = sum(line.m_related_hours for line in rec.application_module)

    @api.multi
    def _a_compute_sum_cost_cooperation(self):
        for rec in self:
            rec.a_related_cost_cooperation = sum(line.m_related_cost_cooperation for line in rec.application_module)


class MaintenanceModuleItems(models.Model):
    _name = 'maintenance.module.items'
    _description = 'Application module items'

    name = fields.Char(string="Module")
    allowed_groups = fields.Many2many('maintenance.application.groups')
    allowed_users = fields.Many2many('hr.employee')
    application = fields.Many2one('maintenance.application')
    module_menu_view = fields.Many2many('maintenance.module.menu')
    m_related_hours = fields.Float(compute='_m_compute_sum_hours_spent',
                                   readonly=True,
                                   track_visibility='onchange')
    m_related_cost_cooperation = fields.Float(compute='_m_compute_sum_cost_cooperation',
                                              readonly=True,
                                              track_visibility='onchange')

    @api.multi
    def _m_compute_sum_hours_spent(self):
        for rec in self:
            rec.m_related_hours = sum(line.related_hours for line in rec.module_menu_view)

    @api.multi
    def _m_compute_sum_cost_cooperation(self):
        for rec in self:
            rec.m_related_cost_cooperation = sum(line.related_cost_cooperation for line in rec.module_menu_view)


class MaintenanceModuleMenu(models.Model):
    _name = 'maintenance.module.menu'
    _description = 'Application module menu'

    name = fields.Char(string="Menu view")
    menu_view = fields.One2many('maintenance.menu.view', 'view_menu')
    related_hours = fields.Float(compute='_compute_sum_hours_spent',
                                 readonly=True,
                                 track_visibility='onchange')
    related_cost_cooperation = fields.Float(compute='_compute_sum_cost_cooperation',
                                            readonly=True,
                                            track_visibility='onchange')

    @api.multi
    def _compute_sum_hours_spent(self):
        for rec in self:
            rec.related_hours = sum(line.hours_spent for line in rec.menu_view)

    @api.multi
    def _compute_sum_cost_cooperation(self):
        for rec in self:
            rec.related_cost_cooperation = sum(line.cost_cooperation for line in rec.menu_view)


class MaintenanceMenuView(models.Model):
    _name = 'maintenance.menu.view'
    _description = 'Application menu view items'

    name = fields.Char(string="View name")
    view_version = fields.Char(string="View version")
    change_description = fields.Text(string="Description")
    hours_spent = fields.Float(string='Hours Spent', )
    cost_cooperation = fields.Float(string='Cost')
    view_menu = fields.Many2one('maintenance.module.menu')
    related_issue = fields.Many2one('project.issue', store='True')


class MaintenanceApplicationGroups(models.Model):
    _name = 'maintenance.application.groups'
    _description = 'Application groups'

    name = fields.Char(string="Group name")
    allowed_users = fields.Many2many('hr.employee')
    allowed_create = fields.Boolean(string="Create")
    allowed_edit = fields.Boolean(string="Edit")
    allowed_read = fields.Boolean(string="Read")
    allowed_delete = fields.Boolean(string="Delete")


class MaintenanceDatabase(models.Model):
    _name = 'maintenance.database'
    _description = 'Database inventory'

    name = fields.Char(string="Database name")
    database_tables = fields.Many2many('maintenance.tables')
    database_application = fields.Many2many('maintenance.application')


class MaintenanceTables(models.Model):
    _name = 'maintenance.tables'
    _description = 'Database tables'

    name = fields.Char(string="Table name")
    table_fields = fields.Many2many('maintenance.table.fields')
    table_menu_item = fields.Many2many('maintenance.module.items')


class MaintenanceTableFields(models.Model):
    _name = 'maintenance.table.fields'
    _description = 'Fields for table'

    name = fields.Char(string="Field name")


class MaintenanceComponentType(models.Model):
    _name = 'maintenance.component.type'

    name = fields.Char(string='Component type')


class MaintenanceEquipmentTracking(models.Model):
    _name = 'maintenance.equipment.tracking'

    sm_equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')

    tool_shop_id = fields.Many2one('maintenance.tool.shop', string='Tool shop')

    sm_equipment_assign_to = fields.Selection([('employee', 'Employee'), ('other', 'Other')],
                                              string='Used By',
                                              required=True,
                                              default='other')
    sm_employee_id = fields.Many2one('hr.employee', string='Assigned to Employee', track_visibility='onchange')
    sm_department_id = fields.Many2one('hr.department', string='Assigned to Department', track_visibility='onchange')
    sm_employee_number = fields.Char('hr.employee', related='sm_employee_id.employee_number', readonly=True, store=True)
    sm_department_number = fields.Char('hr.department',
                                       related='sm_department_id.department_code',
                                       readonly=True,
                                       store=True)
    employee_department_sm = fields.Many2one('hr.department',
                                             compute='_compute_sm_department_id',
                                             readonly=True,
                                             store=True)
    employee_department_sm_number = fields.Char('hr.department',
                                                related='employee_department_sm.department_code',
                                                readonly=True,
                                                store=True)
    smo_employee_id = fields.Many2one('hr.employee', string='Assigned to Employee', track_visibility='onchange')
    smo_department_id = fields.Many2one('hr.department', string='Assigned to Department', track_visibility='onchange')
    smo_employee_number = fields.Char('hr.employee',
                                      related='smo_employee_id.employee_number',
                                      readonly=True,
                                      store=True)
    smo_department_number = fields.Char('hr.department',
                                        related='smo_department_id.department_code',
                                        readonly=True,
                                        store=True)
    employee_department_smo = fields.Many2one('hr.department',
                                              compute='_compute_smo_department_id',
                                              readonly=True,
                                              store=True)
    employee_department_smo_number = fields.Char('hr.department',
                                                 related='employee_department_smo.department_code',
                                                 readonly=True,
                                                 store=True)

    @api.depends('sm_employee_id')
    def _compute_sm_department_id(self):
        for equipment in self:
            if equipment.sm_employee_id:
                equipment.employee_department_sm = equipment.sm_employee_id.department_id
            else:
                equipment.employee_department_sm = False

    @api.depends('smo_employee_id')
    def _compute_smo_department_id(self):
        for equipment in self:
            if equipment.smo_employee_id:
                equipment.employee_department_smo = equipment.smo_employee_id.department_id
            else:
                equipment.employee_department_smo = False


class MaintenanceToolShop(models.Model):
    _name = 'maintenance.tool.shop'

    name = fields.Char(string='Tool shop')
    equipment_tracking_ids = fields.One2many('maintenance.equipment.tracking',
                                             'tool_shop_id',
                                             string="Tool Shop Equipment")

    equipment_tracking_ts_info_lines = fields.Many2many('tool.shop.equipment.count',
                                                        string='Tool shop equipment count',
                                                        compute='_compute_tracking_info_lines')

    @api.depends('equipment_tracking_ids')
    def _compute_tracking_info_lines(self):
        """Compute temporary tool shop equipment count values"""
        """Problem kada nije dodjeljeno barem na jedan employee ne prikazuje vrijednosti ostalo radi"""
        tsec_model = self.env['tool.shop.equipment.count']
        equipment_tracking_ts_info_lines = tsec_model
        if not self.equipment_tracking_ids:
            return
        data_lines = self.env['maintenance.equipment.tracking'].read_group(
            [('tool_shop_id', '=', self.id)],
            ['sm_equipment_id', 'tool_shop_id', 'number_of_pieces'],
            ['sm_equipment_id'])
        res = dict((data['sm_equipment_id'][0], data['sm_equipment_id_count'] or 0)
                   for data in data_lines)
        data_employee_lines = self.env['maintenance.equipment.tracking'].read_group(
            [('tool_shop_id', '=', self.id), ('sm_equipment_assign_to', '=', 'employee')],
            ['sm_equipment_id', 'tool_shop_id', 'number_of_piecese'],
            ['sm_equipment_id'])
        res_employee = dict((data['sm_equipment_id'][0], data['sm_equipment_id_count'])
                            for data in data_employee_lines)
        for sm_equipment_id in res:
            vals = {'tool_shop_id': self.id,
                    'count': res[sm_equipment_id],
                    'count_employee': res_employee.get(sm_equipment_id, 0),
                    'sm_equipment_id': sm_equipment_id}
            temp_res = tsec_model.create(vals)
            if temp_res:
                equipment_tracking_ts_info_lines |= temp_res
        self.equipment_tracking_ts_info_lines = equipment_tracking_ts_info_lines


class ToolShopMaintenanceEquipmentCount(models.TransientModel):
    _name = 'tool.shop.equipment.count'
    _description = """Temporary model to display tool shop
     equipment data without storing"""

    tool_shop_id = fields.Many2one('maintenance.tool.shop', string='Tool shop')
    sm_equipment_id = fields.Many2one('maintenance.equipment', string='Equipment')
    count = fields.Integer(string='Count')
    count_employee = fields.Integer(string='Used By Employee')

    @api.depends('count', 'count_employee')
    def _compute_equipment_on_storage(self):
        for equipment in self:
            equipment.on_storage = self.count - self.count_employee

    on_storage = fields.Integer(string='On storage', compute='_compute_equipment_on_storage')


""" Work in progress
class MaintenanceMobileCost(models.Model):
    _name = 'maintenance.mobile.cost'
    _description = 'Mobile bill specification'

    mobile_long = fields.Char(string='Subscriber number')
    invoice_number = fields.Char(string='Invoice number')
    invoice_date = fields.Date(string='Date of invoice')

    subscriber_total = fields.Char(string='Subscriber total')
    quantity_tf = fields.Char(string='Quantity tax free')
    total_tf = fields.Char(string='Total tax free')

    quantity_month_discount = fields.Char(string='Quantity monthly discount')
    total_month_discount = fields.Char(string='Total monthly discount')

    quantity_vpn = fields.Char(string='Quantitiy VPN')
    total_vpn = fields.Char(string='Total cost VPN')

    duration_call_network = fields.Char(string='Calls duration in network')
    total_call_network = fields.Char(string='Total cost calls in network')

    total_cost_vpn = fields.Char(string='Total cost calls in VPN')

    duration_call_fixnet = fields.Char(string='Calls duration to fixed network')
    total_call_fixnet = fields.Char(string='Total cost to fixed network')

    duration_call_onet = fields.Char(string='Calls duration to other mobile networks')
    total_call_onet = fields.Char(string='Total cost to other mobile networks')

    duration_call_roaming = fields.Char(string='Calls duration to roaming')
    total_call_roaming = fields.Char(string='Total cost to roaming')

    duration_call_special = fields.Char(string='Calls duration to special numbers')
    total_call_special = fields.Char(string='Total cost call to special numbers')

    total_services_roaming = fields.Char(string='Total cost roaming services')

    quantity_sms = fields.Char(string='Sent SMS quantity')
    total_sms = fields.Char(string='Total cost of SMS')

    quantity_sms_av = fields.Char(string='Sent SMS quantity with added value')
    total_sms_av = fields.Char(string='Total cost of SMS with added value')

    quantity_mms = fields.Char(string='Sent MMS quantity')
    total_mms = fields.Char(string='Total cost of MMS')

    quantity_mms_av = fields.Char(string='Sent MMS quantity with added value')
    total_mms_av = fields.Char(string='Total cost of MMS with added value')

    quantity_data = fields.Char(string='Quantity of data transfer')
    total_data = fields.Char(string='Total cost of data transfer')

    total_other_services = fields.Char(string='Other services total')

    quantity_network_access = fields.Char(string='Quantity for network access')
    total_network_access = fields.Char(string='Total for network access')

    quantity_network_frequency = fields.Char(string='Quantity network frequency')
    total_network_frequency = fields.Char(string='Total network frequency')
"""