# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parser
import time
from odoo import api, models, fields, osv, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
from odoo.exceptions import UserError


class VLHRSubcontractorsPlan(models.Model):
    _name = 'vl.hr.subcontractors.plan'
    _description = "Plan of evaluation"
    name = fields.Char("Plan of evaluation", required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True)
    phase_ids = fields.One2many('vl.hr.subcontractors.plan.phase', 'plan_id', 'Appraisal Phases', copy=True),
    month_firs = fields.Integer('First Appraisal in (months)',
                                help="This number of months will be used to schedule the first evaluation date of the "
                                     "employee when selecting an evaluation plan. "),
    month_next = fields.Integer('Periodicity of Appraisal (months)',
                                help="The number of month that depicts the delay between each evaluation of this plan "
                                     "(after the first one)."),
    active = fields.Boolean('Active')

    defaults = {
        'active': True,
        'month_first': 6,
        'month_next': 12,
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company').company_default.get(cr, uid, 'account.account',
                                                                                          context=c),
                }


class VLHRSubcontractorsPlanPhase(models.Model):
    _name = "vl.hr.subcontractors.plan.phase"
    _description = "Plan of evaluation Phase"
    order = "sequence"
    name_phase = fields.Char("Phase", required=True),
    sequence = fields.Integer("Sequence"),
    company_id = fields.Many2one('plan_id', 'company_id', comodel_name='res.company', string='Company', store=True,
                                 readonly=True),
    plan_id = fields.Many2one('vl.hr.subcontractors.plan', 'Appraisal Plan', ondelete='cascade'),
    action = fields.Selection([
            ('top-down', 'Top-Down Appraisal Requests'),
            ('bottom-up', 'Bottom-Up Appraisal Requests'),
            ('self', 'Self Appraisal Requests'),
            ('final', 'Final Interview')], 'Action', required=True),
    survey_id = fields.Many2one('survey.survey', 'Appraisal Form', required=True),
    send_answer_manager = fields.Boolean('All Answers', help="Send all answers to the manager"),
    send_answer_employee = fields.Boolean('All Answers', help="Send all answers to the employee"),
    send_anonymous_manager = fields.Boolean('Anonymous Summary', help="Send an anonymous summary to the manager"),
    send_anonymous_employee = fields.Boolean('Anonymous Summary', help="Send an anonymous summary to the employee"),
    wait = fields.Boolean('Wait Previous Phases', help="Check this box if you want to wait that all preceding phases "
                                                       "are finished before launching this phase."),
    mail_feature = fields.Boolean('Send mail for this phase', help="Check this box if you want to send mail to "
                                                                   "employees coming under this phase"),
    mail_body = fields.Text('Email'),
    email_subject = fields.Text('Subject')

    defaults = {
        'sequence': 1,
        'email_subject': _('''Regarding '''),
        'mail_body': lambda *a: _('''
                                    Date: %(date)s
                                    Dear %(employee_name)s,
                                    I am doing an evaluation regarding %(eval_name)s.
                                    Kindly submit your response.
                                    Thanks,
                                    --
                                    %(user_signature)s
                                  '''),
                }


class HREmployee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    @api.multi
    def _appraisal_count(self, cr, uid, ids,  # field_name, arg,
                         context=None):
        evaluation = self['vl.hr.evaluation.interview']
        return {
            employee_id: evaluation.search_count(cr, uid, [('user_to_review_id', '=', employee_id)], context=context)
            for employee_id in ids
        }
    evaluation_plan_id = fields.Many2one('vl.hr.subcontractors.plan', 'Appraisal Plan'),
    evaluation_date = fields.Date('Next Appraisal Date', help="The date of the next appraisal is computed by the "
                                                              "appraisal plan's dates (first appraisal periodicity)."),
    appraisal_count = _appraisal_count(type='integer', string='Appraisal Interviews'),

    @api.multi
    def run_subcontractor_evaluation(self, cr, uid,  # automatic=False, use_new_cursor=False,
                                     context=None):  #cronjob
        now = parser.parse[datetime.now().strftime('%Y-%m-%d')]
        obj_evaluation = self['vl.hr.evaluation']
        emp_ids = self.search(cr, uid, [('evaluation_plan_id', '<>', False), ('evaluation_date', '=', False)],
                              context=context)
        for emp in self.browse(cr, uid, emp_ids, context=context):
            first_date = (now + relativedelta(months=emp.evaluation_plan_id.month_first)).strftime('%Y-%m-%d')
            self.write(cr, uid, [emp.id], {'evaluation_date': first_date}, context=context)

            emp_ids = self.search(cr, uid, [('evaluation_plan_id', '<>', False), ('evaluation_date', '<=',
                                                                        time.strftime("%Y-%m-%d"))], context=context)
        for emp in self.browse(cr, uid, emp_ids, context=context):
            next_date = (now + relativedelta(months=emp.evaluation_plan_id.month_next)).strftime('%Y-%m-%d')
            self.write(cr, uid, [emp.id], {'evaluation_date': next_date}, context=context)
            plan_id = obj_evaluation.create(cr, uid, {'employee_id': emp.id, 'plan_id': emp.evaluation_plan_id.id},
                                            context=context)
            obj_evaluation.button_plan_in_progress(cr, uid, [plan_id], context=context)
        return True


class VLHREvaluation(models.Model):
    _name = "vl.hr.evaluation"
    _inherit = "mail.thread"
    _description = "Employee Appraisal"
    _rec_name = "employee_id"
    date = fields.Date("Appraisal Deadline", required=True, index=True),
    employee_id = fields.Many2one('hr.employee', "Employee", required=True),
    note_summary = fields.Text('Appraisal Summary'),
    note_action = fields.Text('Action Plan', help="If the evaluation does not meet the expectations, you can "
                                                  "propose an action plan"),
    rating = fields.Selection([
            ('0', 'Significantly below expectations'),
            ('1', 'Do not meet expectations'),
            ('2', 'Meet expectations'),
            ('3', 'Exceeds expectations'),
            ('4', 'Significantly exceeds expectations'),
        ], "Appreciation", help="This is the appreciation on which the evaluation is summarized."),
    survey_request_ids = fields.One2many('vl.hr.evaluation.interview', 'evaluation_id', 'Appraisal Forms'),
    plan_id = fields.Many2one('vl.hr.subcontractors.plan', 'Plan', required=True),
    state = fields.Selection([
            ('draft', 'New'),
            ('cancel', 'Cancelled'),
            ('wait', 'Plan In Progress'),
            ('progress', 'Waiting Appreciation'),
            ('done', 'Done'),
        ], 'Status', required=True, readonly=True, copy=False),
    date_close = fields.Date('Ending Date', index=True),
    defaults = {
        'date': lambda *a: (parser.parse(datetime.now().strftime('%Y-%m-%d')) + relativedelta(months=+1)).strftime(
            '%Y-%m-%d'),
        'state': lambda *a: 'draft',
                }

    @api.multi
    def _name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.browse(cr, uid, ids, context=context)
        res = []
        for record in reads:
            name = record.plan_id.name
            employee = record.employee_id.name_related
            res.append((record['id'], name + ' / ' + employee))
        return res

    @api.multi
    def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
        vals = {}
        vals['plan_id'] = False
        if employee_id:
            employee_obj = self['hr.employee']
            for employee in employee_obj.browse(cr, uid, [employee_id], context=context):
                if employee and employee.evaluation_plan_id and employee.evaluation_plan_id.id:
                    vals.update({'plan_id': employee.evaluation_plan_id.id})
        return {'value': vals}

    @api.multi
    def button_plan_in_progress(self, cr, uid, ids, context=None):
        hr_eval_inter_obj = self['vl.hr.evaluation.interview']
        if context is None:
            context = {}
        for evaluation in self.browse(cr, uid, ids, context=context):
            wait = False
            for phase in evaluation.plan_id.phase_ids:
                children = []
                if phase.action == "bottom-up":
                    children = evaluation.employee_id.child_ids
                elif phase.action in ("top-down", "final"):
                    if evaluation.employee_id.parent_id:
                        children = [evaluation.employee_id.parent_id]
                elif phase.action == "self":
                    children = [evaluation.employee_id]
                for child in children:

                    int_id = hr_eval_inter_obj.create(cr, uid, {
                        'evaluation_id': evaluation.id,
                        'phase_id': phase.id,
                        'deadline': (parser.parse(datetime.now().strftime('%Y-%m-%d')) + relativedelta(
                            months=+1)).strftime('%Y-%m-%d'),
                        'user_id': child.user_id.id,
                    }, context=context)
                    if phase.wait:
                        wait = True
                    if not wait:
                        hr_eval_inter_obj.survey_req_waiting_answer(cr, uid, [int_id], context=context)

                    if (not wait) and phase.mail_feature:
                        body = phase.mail_body % {'employee_name': child.name,
                                                  'user_signature': child.user_id.signature,
                                                  'eval_name': phase.survey_id.title, 'date': time.strftime('%Y-%m-%d'),
                                                  'time': time}
                        sub = phase.email_subject
                        if child.work_email:
                            vals = {'state': 'outgoing',
                                    'subject': sub,
                                    'body_html': '<pre>%s</pre>' % body,
                                    'email_to': child.work_email,
                                    'email_from': evaluation.employee_id.work_email}
                            self['mail.mail'].create(cr, uid, vals, context=context)

        self.write(cr, uid, ids, {'state': 'wait'}, context=context)
        return True

    @api.multi
    def button_final_validation(self, cr, uid, ids, context=None):
        request_obj = self['vl.hr.evaluation.interview']
        self.write(cr, uid, ids, {'state': 'progress'}, context=context)
        for evaluation in self.browse(cr, uid, ids, context=context):
            if evaluation.employee_id and evaluation.employee_id.parent_id and evaluation.employee_id.parent_id.user_id:
                self.message_subscribe_users(cr, uid, [evaluation.id],
                                             user_ids=[evaluation.employee_id.parent_id.user_id.id], context=context)
            if len(evaluation.survey_request_ids) != len(request_obj.search(cr, uid,
                                                                            [('evaluation_id', '=', evaluation.id),
                                                                             ('state', 'in', ['done', 'cancel'])],
                                                                            context=context)):
                raise UserError(_("You cannot change state, because some appraisal forms have not been completed."))
        return True

    @api.multi
    def button_done(self, cr, uid, ids,  # context=None
                    ):
        self.write(cr, uid, ids, ({'state': 'done'}))
        self.date_close = time.strftime('%Y-%m-%d')  # , context=context)}
        return True

    @api.multi
    def button_cancel(self, cr, uid, ids, context=None):
        interview_obj = self['vl.hr.evaluation.interview']
        evaluation = self.browse(cr, uid, ids[0], context)
        interview_obj.survey_req_cancel(cr, uid, [r.id for r in evaluation.survey_request_ids])
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True

    @api.multi
    def button_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True

    @api.multi
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('employee_id'):
            employee_id = self['hr.employee'].browse(cr, uid, vals.get('employee_id'), context=context)
            if employee_id.parent_id and employee_id.parent_id.user_id:
                vals['message_follower_ids'] = [(4, employee_id.parent_id.user_id.partner_id.id)]
        if 'date' in vals:
            new_vals = {'deadline': vals.get('date')}
            obj_hr_eval_iterview = self['vl.hr.evaluation.interview']
            for evaluation in self.browse(cr, uid, ids, context=context):
                for survey_req in evaluation.survey_request_ids:
                    obj_hr_eval_iterview.write(cr, uid, [survey_req.id], new_vals, context=context)
        return super(VLHREvaluation, self).write(cr, uid, ids, vals, context=context)


class VLHREvaluationInterview(models.Model):
    _name = 'vl.hr.evaluation.interview'
    _inherit = 'mail.thread'
    _rec_name = 'user_to_review_id'
    _description = 'Appraisal Interview'
    request_id = fields.Many2one('survey.user_input', 'Survey Request', ondelete='cascade', readonly=True),
    evaluation_id = fields.Many2one('vl.hr.evaluation', 'Appraisal Plan', required=True),
    phase_id = fields.Many2one('vl.hr.subcontractors.plan.phase', 'Appraisal Phase', required=True),
    user_to_review_id = fields.Many2one('evaluation_id', 'employee_id', comodel_name="hr.employee",
                                        string="Employee to evaluate"),
    user_id = fields.Many2one('res.users', 'Interviewer'),
    state = fields.Selection([('draft', "Draft"), ('waiting_answer', "In progress"), ('done', "Done"),
                              ('cancel', "Cancelled")], string="State", required=True, copy=False),
    survey_id = fields.Many2one('phase_id', 'survey_id', string="Appraisal Form", comodel_name="survey.survey"),
    deadline = fields.Reference('request_id', 'deadline', type="datetime", string="Deadline"),
    defaults = {
        'state': 'draft'
                }

    @api.multi
    def create(self, cr, uid, vals, context=None):
        phase_obj = self['vl.hr.subcontractors.plan.phase']
        survey_id = phase_obj.read(cr, uid, vals.get('phase_id'), fields=['survey_id'], context=context)['survey_id'][0]

        if vals.get('user_id'):
            user_obj = self['res.users']
            partner_id = user_obj.read(cr, uid, vals.get('user_id'), fields=['partner_id'],
                                       context=context)['partner_id'][0]
        else:
            partner_id = None

        user_input_obj = self['survey.user_input']

        if not vals.get('deadline'):
            vals['deadline'] = (datetime.now() + timedelta(days=28)).strftime(DF)

        ret = user_input_obj.create(cr, uid, {'survey_id': survey_id,
                                              'deadline': vals.get('deadline'),
                                              'type': 'link',
                                              'partner_id': partner_id}, context=context)
        vals['request_id'] = ret
        return super(VLHREvaluationInterview, self).create(cr, uid, vals, context=context)

    @api.multi
    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.browse(cr, uid, ids, context=context)
        res = []
        for record in reads:
            name = record.survey_id.title
            res.append((record['id'], name))
        return res

    @api.multi
    def survey_req_waiting_answer(self, cr, uid, ids, context=None):
        request_obj = self['survey.user_input']
        for interview in self.browse(cr, uid, ids, context=context):
            if interview.request_id:
                request_obj.action_survey_resent(cr, uid, [interview.request_id.id], context=context)
            self.write(cr, uid, interview.id, {'state': 'waiting_answer'}, context=context)
        return True

    @api.multi
    def survey_req_done(self, cr, uid, ids, context=None):
        for id in self.browse(cr, uid, ids, context=context):
            flag = False
            wating_id = 0
            if not id.evaluation_id.id:  # raise models.expression(_('Warning!'), _
                # ("You cannot start evaluation without Appraisal."))
                records = id.evaluation_id.survey_request_ids
                for child in records:
                    if child.state == "draft":
                        wating_id = child.id
                    continue
            if child.state != "done":
                flag = True
            if not flag and wating_id:
                self.survey_req_waiting_answer(cr, uid, [wating_id], context=context)
        self.write(cr, uid, ids, {'state': 'done'}, context=context)
        return True

    @api.multi
    def survey_req_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
        return True

    @api.multi
    def action_print_survey(self, cr, uid, ids, context=None):
        """ If response is available then print this response otherwise print survey form
        (print template of the survey) """
        context = dict(context or {})
        interview = self.browse(cr, uid, ids, context=context)[0]
        survey_obj = self['survey.survey']
        response_obj = self['survey.user_input']
        response = response_obj.browse(cr, uid, interview.request_id.id, context=context)
        context.update({'survey_token': response.token})
        return survey_obj.action_print_survey(cr, uid, [interview.survey_id.id], context=context)

    @api.multi
    def action_start_survey(self, cr, uid, ids, context=None):
        context = dict(context or {})
        interview = self.browse(cr, uid, ids, context=context)
        survey_obj = self['survey.survey']
        response_obj = self['survey.user_input']
        # grab the token of the response and start surveying
        response = response_obj.browse(cr, uid, interview.request_id.id, context=context)
        context.update({'survey_token': response.token})
        return survey_obj.action_start_survey(cr, uid, [interview.survey_id.id], context=context)




    # @api.multi
    # def action_start_survey(self):
    #    self.ensure_one()
    #    # create a response and link it to this applicant
    #    if not self.response_id:
    #        response = self.env['survey.user_input'].create(
    #            {'survey_id': self.survey_id.id})
    #        self.response_id = response.id
    #    else:
    #        response = self.response_id
    #    # grab the token of the response and start surveying
    #    return self.survey_id.with_context(survey_token=response.token).action_start_survey()