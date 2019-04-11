# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
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

    period_day = fields.Integer('Daily maintenance')
    period_week = fields.Integer('Weekly maintenance')
    period_month = fields.Integer('Monthly maintenance')
    period_quater = fields.Integer('Quaterly maintenance')
    period_half = fields.Integer('Half year maintenance')
    period_year = fields.Integer('Yearly maintenance')

    next_action_date_day = fields.Datetime(compute='_compute_next_issue_day',
                                           string='Date of the next preventive issue', readonly=True, store=True,
                                           track_visibility='onchange')
    next_action_date_week = fields.Datetime(compute='_compute_next_issue_week',
                                           string='Date of the next preventive issue', readonly=True, store=True,
                                           track_visibility='onchange')
    next_action_date_month = fields.Datetime(compute='_compute_next_issue_month',
                                           string='Date of the next preventive issue', readonly=True, store=True,
                                           track_visibility='onchange')
    next_action_date_quater = fields.Datetime(compute='_compute_next_issue_quater',
                                           string='Date of the next preventive issue', readonly=True, store=True,
                                           track_visibility='onchange')
    next_action_date_half = fields.Datetime(compute='_compute_next_issue_half',
                                           string='Date of the next preventive issue', readonly=True, store=True,
                                           track_visibility='onchange')
    next_action_date_year = fields.Datetime(compute='_compute_next_issue_year',
                                           string='Date of the next preventive issue', readonly=True, store=True,
                                           track_visibility='onchange')

    next_action_dates = fields.Datetime(compute='_compute_next_issue_day',
                                        string='Date of the next preventive issue', readonly=True, store=True,
                                        track_visibility='onchange')

    description_day = fields.Text('What needs to be maintained?')
    description_week = fields.Text('What needs to be maintained?')
    description_month = fields.Text('What needs to be maintained?')
    description_quater = fields.Text('What needs to be maintained?')
    description_half = fields.Text('What needs to be maintained?')
    description_year = fields.Text('What needs to be maintained?')


    @api.depends('period_day', 'preventive_issue_ids.date', 'preventive_issue_ids.date_done_iss')
    def _compute_next_issue_day(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period_day > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done'),
                ('date_done_iss', '=', False)], order="date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done'),
                ('date_done_iss', '!=', False)], order="date_done_iss desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_day) * 2 and fields.Date.from_string \
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=equipment.period_day) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=equipment.period_day))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_day) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=equipment.period_day))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(days=equipment.period_day)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(fields.Date.from_string(date_now) + timedelta(days=equipment.period_day))

            equipment.next_action_date_day = next_date

    @api.depends('period_week', 'preventive_issue_ids.date', 'preventive_issue_ids.date_done_iss')
    def _compute_next_issue_week(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period_week > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done'),
                ('date_done_iss', '=', False)], order="date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done'),
                ('date_done_iss', '!=', False)], order="date_done_iss desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period_week) * 2 and fields.Date.from_string \
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=equipment.period_week) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=equipment.period_week))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_week) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=equipment.period_week))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                    days=equipment.period_week)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(
                    fields.Date.from_string(date_now) + timedelta(days=equipment.period_week))

            equipment.next_action_date_week = next_date

    @api.depends('period_month', 'preventive_issue_ids.date', 'preventive_issue_ids.date_done_iss')
    def _compute_next_issue_month(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period_month > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done'),
                ('date_done_iss', '=', False)], order="date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done'),
                ('date_done_iss', '!=', False)], order="date_done_iss desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period_month) * 2 and fields.Date.from_string \
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=equipment.period_month) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=equipment.period_month))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_month) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=equipment.period_month))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                    days=equipment.period_month)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(
                    fields.Date.from_string(date_now) + timedelta(days=equipment.period_month))

            equipment.next_action_date_month = next_date

    @api.depends('period_quater', 'preventive_issue_ids.date', 'preventive_issue_ids.date_done_iss')
    def _compute_next_issue_quater(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period_quater > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done'),
                ('date_done_iss', '=', False)], order="date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done'),
                ('date_done_iss', '!=', False)], order="date_done_iss desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period_quater) * 2 and fields.Date.from_string \
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=equipment.period_quater) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=equipment.period_quater))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_quater) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=equipment.period_quater))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                    days=equipment.period_quater)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(
                    fields.Date.from_string(date_now) + timedelta(days=equipment.period_quater))

            equipment.next_action_date_quater = next_date

    @api.depends('period_half', 'preventive_issue_ids.date', 'preventive_issue_ids.date_done_iss')
    def _compute_next_issue_half(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period_half > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done'),
                ('date_done_iss', '=', False)], order="date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done'),
                ('date_done_iss', '!=', False)], order="date_done_iss desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period_half) * 2 and fields.Date.from_string \
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=equipment.period_half) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=equipment.period_half))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_half) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=equipment.period_half))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                    days=equipment.period_half)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(
                    fields.Date.from_string(date_now) + timedelta(days=equipment.period_half))

            equipment.next_action_date_half = next_date

    @api.depends('period_year', 'preventive_issue_ids.date', 'preventive_issue_ids.date_done_iss')
    def _compute_next_issue_year(self):

        date_now = fields.Date.context_today(self)
        for equipment in self.filtered(lambda x: x.period_year > 0):
            next_issue_todo = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '!=', 'done'),
                ('date_done_iss', '=', False)], order="date asc", limit=1)
            last_issue_done = self.env['project.issue'].search([
                ('equipment_id', '=', equipment.id),
                ('issue_type', '=', 'preventive'),
                ('state', '=', 'done'),
                ('date_done_iss', '!=', False)], order="date_done_iss desc", limit=1)
            if next_issue_todo and last_issue_done:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    last_issue_done.date_done_iss)
                if date_gap > timedelta(0) and date_gap > timedelta(
                        days=equipment.period_year) * 2 and fields.Date.from_string \
                            (next_issue_todo.date) > fields.Date.from_string(date_now):
                    if fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                            days=equipment.period_year) < fields.Date.from_string(date_now):
                        next_date = date_now
                    else:
                        next_date = fields.Date.to_string(
                            fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                                days=equipment.period_year))
            elif next_issue_todo:
                next_date = next_issue_todo.date
                date_gap = fields.Date.from_string(next_issue_todo.date) - fields.Date.from_string(
                    date_now)
                if date_gap > timedelta(0) and date_gap > timedelta(days=equipment.period_year) * 2:
                    next_date = fields.Date.to_string(
                        fields.Date.from_string(date_now) + timedelta(days=equipment.period_year))
            elif last_issue_done:
                next_date = fields.Date.from_string(last_issue_done.date_done_iss) + timedelta(
                    days=equipment.period_year)
                if next_date < fields.Date.from_string(date_now):
                    next_date = date_now
            else:
                next_date = fields.Date.to_string(
                    fields.Date.from_string(date_now) + timedelta(days=equipment.period_year))

            equipment.next_action_date_year = next_date

    @api.model
    def _create_new_issue_day(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'description': self.description_day,
            #'issuer_id.name': 'Administrator',
        })

    @api.model
    def _create_new_issue_week(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'description': self.description_week,
            # 'issuer_id.name': 'Administrator',
        })

    @api.model
    def _create_new_issue_month(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'description': self.description_month,
            # 'issuer_id.name': 'Administrator',
        })

    @api.model
    def _create_new_issue_quater(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'description': self.description_quater,
            # 'issuer_id.name': 'Administrator',
        })

    @api.model
    def _create_new_issue_half(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'description': self.description_half,
            # 'issuer_id.name': 'Administrator',
        })

    @api.model
    def _create_new_issue_year(self, date):
        self.ensure_one()
        self.env['project.issue'].create({
            'name': _('Preventive issue - %s') % self.name,
            'date': date,
            'equipment_id': self.id,
            'issue_type': 'preventive',
            'description': self.description_year,
            # 'issuer_id.name': 'Administrator',
        })

    @api.model
    def _cron_generate_issue_day(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period_day', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state', '!=', 'done'),
                                                              ('equipment_id', '=', equipment.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', equipment.next_action_date_day)])
            if not next_requests:
                equipment._create_new_issue_day(equipment.next_action_date_day)

    @api.model
    def _cron_generate_issue_week(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period_week', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state', '!=', 'done'),
                                                              ('equipment_id', '=', equipment.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', equipment.next_action_date_week)])
            if not next_requests:
                equipment._create_new_issue_week(equipment.next_action_date_week)

    @api.model
    def _cron_generate_issue_month(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period_month', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state', '!=', 'done'),
                                                              ('equipment_id', '=', equipment.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', equipment.next_action_date_month)])
            if not next_requests:
                equipment._create_new_issue_month(equipment.next_action_date_month)

    @api.model
    def _cron_generate_issue_quater(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period_quater', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state', '!=', 'done'),
                                                              ('equipment_id', '=', equipment.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', equipment.next_action_date_quater)])
            if not next_requests:
                equipment._create_new_issue_quater(equipment.next_action_date_quater)

    @api.model
    def _cron_generate_issue_half(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period_half', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state', '!=', 'done'),
                                                              ('equipment_id', '=', equipment.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', equipment.next_action_date_half)])
            if not next_requests:
                equipment._create_new_issue_half(equipment.next_action_date_half)

    @api.model
    def _cron_generate_issue_year(self):
        """
            Generates issue request on the next_action_date or today if none exists
        """
        for equipment in self.search([('period_year', '>', 0)]):
            next_requests = self.env['project.issue'].search([('state', '!=', 'done'),
                                                              ('equipment_id', '=', equipment.id),
                                                              ('issue_type', '=', 'preventive'),
                                                              ('date', '=', equipment.next_action_date_year)])
            if not next_requests:
                equipment._create_new_issue_year(equipment.next_action_date_year)

    network_resources = fields.Many2many('maintenance.network.resources')
    location_name = fields.Char(string="Location name")


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


class MaintenanceNetworkResources(models.Model):
    _name = 'maintenance.network.resources'
    _description = 'Shared network resources'

    name = fields.Char(string='Resource name')
    parent_equipment_id = fields.Many2many('maintenance.equipment')
    user_groups = fields.Many2many('maintenance.ad.groups', string='Allowed AD Gropups')
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
    application_menu = fields.One2many('maintenance.menu.items', 'application')


class MaintenanceMenuItems(models.Model):
    _name = 'maintenance.menu.items'
    _description = 'Application menu items'

    name = fields.Char(string="Menu item")
    allowed_groups = fields.Many2many('maintenance.application.groups')
    allowed_users = fields.Many2many('hr.employee')
    application = fields.Many2one('maintenance.application', 'application_menu')


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
    table_menu_item = fields.Many2many('maintenance.menu.items')


class MaintenanceTableFields(models.Model):
    _name = 'maintenance.table.fields'
    _description = 'Fields for table'

    name = fields.Char(string="Field name")


class MaintenanceComponentType(models.Model):
    _name = 'maintenance.component.type'

    name = fields.Char(string='Component type')
