# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models, fields, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_number = fields.Char(string='Employee ID number', required=True)
    employee_number_long = fields.Char(string='Employee ID number long', required=True)
    employee_mifare_card_number = fields.Char(string='Employe MIFARE card number')

    # empass_equipement_ids = fields.Many2one('maintenance.equipment', 'employee_id', string='Assigned equipment')
    employee_assigned_equipment_ids = fields.One2many('maintenance.equipment', 'employee_id'
                                                      #string='Assigned equipment'
                                                      )

    work_phone_short = fields.Char('Work Phone Short')
    mobile_phone_short = fields.Char('Work Mobile Short')

    history_job_ids = fields.One2many('hr.job.history', 'job_history')
    job_long_id = fields.Many2one('hr.job.long', string='Job Title')

    youth = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no')
    disability = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no')


class HrDepartment(models.Model):
    _name = 'hr.department'
    _inherit = ['hr.department', 'website.published.mixin']

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

    department_code = fields.Char(string="Department Code", required=False)

    department_assigned_equipment_ids = fields.One2many('maintenance.equipment', 'department_id'
                                                        #string='Assigned equipment'
                                                        )

    employee_id = fields.One2many('hr.employee', 'department_id')

    website_published = fields.Boolean(default=False)

    department_job = fields.Many2many('hr.job.long', 'job_id')


class HrJobHistory(models.Model):
    _name = 'hr.job.history'
    _description = 'Job history for employee'

    job_history = fields.Many2one('hr.employee')
    job_id = fields.Many2one('hr.job.long')
    date_start = fields.Date('Date start')
    date_stop = fields.Date('Date stop')
    mobile_short = fields.Many2one('maintenance.equipment', 'pc_number')


class HrJobLong(models.Model):
    _name = 'hr.job.long'
    _description = "Job Position Description"
    _inherit = ['mail.thread']

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

    """From HR.JOB"""
    name = fields.Char(string='Job Title', required=True, index=True, translate=True)
    no_of_employee = fields.Integer(compute='_compute_employees', string="Current Number of Employees", store=True,
                                    help='Number of employees currently occupying this job position.')
    no_of_female = fields.Integer(compute='_compute_employees', string="Current Number of Female Employees", store=True,
                                  help='Number of female employees currently occupying this job position.')
    no_of_youth = fields.Integer(compute='_compute_employees', string="Current Number of Young Employees", store=True,
                                 help='Number of young employees currently occupying this job position.')
    no_of_disability = fields.Integer(compute='_compute_employees',
                                      string="Current Number of Employees with Disability", store=True,
                                      help='Number of employees currently occupying this job position.')

    employee_ids = fields.One2many('hr.employee', 'job_long_id', string='Employees', groups='base.group_user')
    description = fields.Html(string='Job Description')
    department_id = fields.Many2one('hr.department', string='Department')

    @api.depends('employee_ids.job_long_id', 'employee_ids.active', 'employee_ids.gender',
                 'employee_ids.youth', 'employee_ids.disability')
    def _compute_employees(self):
        employee_data = self.env['hr.employee'].read_group(
            [('job_long_id', 'in', self.ids)], ['job_long_id'], ['job_long_id'])
        result = dict((data['job_long_id'][0], data['job_long_id_count']) for data in employee_data)

        employee_data_f = self.env['hr.employee'].read_group(
            [('job_long_id', 'in', self.ids), ('gender', '=', 'female')], ['job_long_id'], ['job_long_id'])
        result_f = dict((data['job_long_id'][0], data['job_long_id_count']) for data in employee_data_f)

        employee_data_y = self.env['hr.employee'].read_group(
            [('job_long_id', 'in', self.ids), ('youth', '=', 'yes')], ['job_long_id'], ['job_long_id'])
        result_y = dict((data['job_long_id'][0], data['job_long_id_count']) for data in employee_data_y)

        employee_data_d = self.env['hr.employee'].read_group(
            [('job_long_id', 'in', self.ids), ('disability', '=', 'yes')], ['job_long_id'], ['job_long_id'])
        result_d = dict((data['job_long_id'][0], data['job_long_id_count']) for data in employee_data_d)

        for job in self:
            job.no_of_disability = result_d.get(job.id, 0)
            job.no_of_youth = result_y.get(job.id, 0)
            job.no_of_female = result_f.get(job.id, 0)
            job.no_of_employee = result.get(job.id, 0)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        return super(HrJobLong, self).copy(default=default)

    """ 
    _sql_constraints = [
        ('name_company_uniq', 'CHECK(1=1)',
         'The name of the job position must be unique per department in company!'),
    ]
    """

    """Job LONG"""
    history_job_ids = fields.One2many('hr.job.history', 'job_id')

    origin_id = fields.Many2one('hr.job.long', string='Previous version')
    origin_ids = fields.One2many('hr.job.long', 'origin_id')
    active = fields.Boolean('Active', default=True)

    sequence = fields.Integer()
    job_id = fields.Many2one('hr.department')
    department_code = fields.Char('hr.department',
                                  related='department_id.department_code',
                                  readonly=True,
                                  store=True
                                  )

    job_position_code = fields.Char(string='Job position code')
    job_function = fields.Many2one('hr.job.function')
    job_function_code = fields.Char('hr.job.function',
                                    related='job_function.function_code',
                                    readonly=True,
                                    store=True
                                    )
    trade = fields.Many2one('hr.job.trade')
    trade_codes = fields.Char('hr.job.trade',
                              related='trade.trade_code',
                              readonly=True,
                              store=True
                              )
    job_responsible_id = fields.Many2one('hr.job.long', string='Responsible')
    job_child_id = fields.One2many('hr.job.long', 'job_responsible_id', string='Subordinate')

    special_conditions = fields.Selection([('yes', 'Yes'),
                                           ('no', 'No')],
                                          string='Special work conditions',
                                          required=True,
                                          default='no')

    service_experience_calculation = fields.Selection([('12/12', '12/12'),
                                                       ('14/12', '14/12'),
                                                       ('15/12', '15/12'),
                                                       ('16/12', '16/12')],
                                                      string='Service experience is calculated',
                                                      required=True,
                                                      default='12/12')
    job_position_coefficient = fields.Float(string='Job position coefficient')
    addition_harsh_work = fields.Float(string='Addition for harsh work environment')
    working_hours = fields.Selection([('standard', 'Standard'),
                                      ('shifts', 'Shifts'),
                                      ('constant_shifts', 'Constant shifts'),
                                      ('six_dax', 'Six-day workweek')],
                                     string='Working hours',
                                     required=True,
                                     default='standard')
    min_qualifications = fields.Char(string='Minimum qualifications')
    min_work_experience = fields.Char(string='Minimum work experience')
    trail_period = fields.Char(string='Trail period')
    internship = fields.Selection([('yes', 'Yes'),
                                   ('no', 'No')],
                                  string='Internship',
                                  required=True,
                                  default='no')
    special_health = fields.Char(string='Special health condition (ar.3 PUR)')
    proficiency_testing = fields.Selection([('yes', 'Yes'),
                                            ('no', 'No')],
                                           string='Proficiency and skills testing',
                                           required=True,
                                           default='no')
    profession_course_vocation = fields.Char(string='Profession/Course/vocation')
    professional_exam = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')],
                                         string='Professional exam',
                                         required=True,
                                         default='no')
    professional_exam_name = fields.Char(string='Name of the professional exam')
    specialization = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No')],
                                      string='Specialization',
                                      required=True,
                                      default='no')
    specialization_name = fields.Char(string='Specialization name')
    special_knowledge = fields.Char(string='Special knowledge')

    """SIZO PART"""

    daily_work_sch = fields.Selection([('1', 'One shift'),
                                       ('2', 'Two shifts'),
                                       ('3', 'Shifts')],
                                      default='1')
    week_work_hrs = fields.Char()
    longer_work = fields.Selection([('1', 'No'),
                                    ('2', 'When required')],
                                   default='1')
    shorten_shift = fields.Selection([('yes', 'Yes'),
                                      ('no', 'No')],
                                     default='no')
    lunch_break_ids = fields.Many2many('hr.lunch', 'lunch_break_id')
    min_qualifications2 = fields.Char(related='min_qualifications', readonly=True)
    safety_responsible = fields.Selection([('yes', 'Yes'),
                                           ('no', 'No')],
                                          default='no')
    special_conditions2 = fields.Selection(related='special_conditions', readonly=True)
    special_experience_calculation = fields.Selection([('yes', 'Yes'),
                                                       ('no', 'No')],
                                                      default='no')
    service_experience_calculation2 = fields.Selection(related='service_experience_calculation', readonly=True)
    protection_gear = fields.Selection([('yes', 'Yes'),
                                        ('no', 'No')],
                                       default='no')
    computer_work = fields.Selection([('yes', 'Yes'),
                                      ('no', 'No')],
                                     default='no')
    health_check_points = fields.Char()
    health_check_other = fields.Char()
    work_tools_ids = fields.Many2many('hr.work.tools', 'work_tools_id')
    work_materials_ids = fields.Many2many('hr.work.materials', 'work_materials_id')
    work_place_ids = fields.Many2many('hr.work.place', 'work_place_id')
    protection_gear1_ids = fields.Many2many('hr.protection.gear', 'protection_gear1_id', string="Head")
    protection_gear2_ids = fields.Many2many('hr.protection.gear', 'protection_gear2_id', string="Eyes")
    protection_gear3_ids = fields.Many2many('hr.protection.gear', 'protection_gear3_id', string="Ears")
    protection_gear4_ids = fields.Many2many('hr.protection.gear', 'protection_gear4_id', string="Nose")
    protection_gear5_ids = fields.Many2many('hr.protection.gear', 'protection_gear5_id', string="Body")
    protection_gear6_ids = fields.Many2many('hr.protection.gear', 'protection_gear6_id', string="Hands")
    protection_gear7_ids = fields.Many2many('hr.protection.gear', 'protection_gear7_id', string="Feat")
    protection_gear8_ids = fields.Many2many('hr.protection.gear', 'protection_gear8_id', string="Additional")

    mandatory_qualification_ids = fields.Many2many('hr.mandatory.qualification', 'mandatory_qualification_id',
                                                   string="Mandatory education")

    risk_ids = fields.Many2many('hr.risk')

    approver_id = fields.Many2one(copy=False)

    @api.multi
    def button_cancel(self):
        vals = {}
        domain = [('state', '=', 'cancelled')]
        next_stage = self.get_next_stage_id(domain=domain, direction='forward')
        if next_stage:
            vals.update(
                {'stage_id': next_stage.id})
        return self.write(vals)

    @api.multi
    def button_create_document_revision(self):
        vals = {}
        domain = [('state', '=', 'open')]
        next_stage = self.get_next_stage_id(domain=domain)
        vals.update(
            {'stage_id': next_stage.id,
             'approval_ids': [(5,)]})

        return self.write(vals)

    @api.multi
    def create_new_job_description(self):
        ctx = self.env.context.copy()
        ctx['create_new_job_description'] = 'True'
        new_job = self.with_context(ctx).copy()
        # action = self.env.ref_action("")
        action = self.env.ref('vl_hr.action_hr_job_long').read()[0]
        form_view = self.env.ref('vl_hr.view_hr_job_long_form')
        action['views'] = [(form_view.id, 'form')]
        action['res_id'] = new_job.id
        return action

    @api.multi
    def copy(self, default=None):
        if self.env.context.get('create_new_job_description', False):
            default = dict(default or {})
            default['origin_id'] = self.id
        return super(HrJobLong, self).copy(default=default)

    """@api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (copy)") % (self.name)
        return super(HrJobLong, self).copy(default=default)"""


class HrJobFunction(models.Model):
    _name = 'hr.job.function'

    name = fields.Char(string='Job function')
    function_code = fields.Char(string='Job function code')


class HrJobTrade(models.Model):
    _name = 'hr.job.trade'

    name = fields.Char(string='trade')
    trade_code = fields.Char(string='Trade code')

