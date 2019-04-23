# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class EnergyCounter(models.Model):
    _name = 'energy.counter'

    project_id = fields.Many2one('crm.lead', store=True)
    project_code = fields.Char('crm.lead', compute='_compute_project_code', readonly=True, store=True)
    counter_location = fields.Many2one('resource.dock', store=True)
    date_write_start = fields.Datetime(default=lambda self: fields.datetime.now())
    date_write_stop = fields.Datetime(default=lambda self: fields.datetime.now())

    counter_state_start = fields.Integer('Enter the value of the counter on connect')
    counter_state_stop = fields.Integer('Enter the value of the counter on disconnect or the month-end')
    counter_state_start380 = fields.Integer('Enter the value of the counter on connect (380)')
    counter_state_stop380 = fields.Integer('Enter the value of the counter on disconnect or the month-end (380)')
    counter_state_start440 = fields.Integer('Enter the value of the counter on connect (440)')
    counter_state_stop440 = fields.Integer('Enter the value of the counter on disconnect or the month-end (440)')
    counter_state_startgenerator = fields.Integer('Enter the value of the counter on connect (Generator)')
    counter_state_stopgenerator = fields.Integer('Enter the value of the counter on disconnect or the month-end (Generator)')
    counter_state_starthours = fields.Integer('Enter the value of the counter on connect (Working hours)')
    counter_state_stophours = fields.Integer('Enter the value of the counter on disconnect or the month-end (Working hours)')

    project_consumption = fields.Integer(compute='_project_consumption', readonly=True, store=True)
    project_consumption_380 = fields.Integer(compute='_project_consumption_380', readonly=True, store=True)
    project_consumption_440 = fields.Integer(compute='_project_consumption_440', readonly=True, store=True)
    project_consumption_generator = fields.Integer(compute='_project_consumption_generator', readonly=True, store=True)
    project_consumption_hours = fields.Integer(compute='_project_consumption_hours', readonly=True, store=True)

    counter_type = fields.Selection([('electrical', 'Electrical'),
                                    ('water', 'Water'),
                                    ('technical_water', 'Technical Water')],
                                    string='Meter type',
                                    required=True,
                                    default='electrical')

    @api.depends('counter_state_start380', 'counter_state_stop380')
    def _project_consumption_380(self):
        for counter in self:
            if counter.counter_state_stop380 == 0:
                counter.project_consumption_380 = False
            else:
                counter.project_consumption_380 = counter.counter_state_stop380 - counter.counter_state_start380

    @api.depends('counter_state_start440', 'counter_state_stop440')
    def _project_consumption_440(self):
        for counter in self:
            if counter.counter_state_stop440 == 0:
                counter.project_consumption_440 = False
            else:
                counter.project_consumption_440 = counter.counter_state_stop440 - counter.counter_state_start440

    @api.depends('counter_state_startgenerator', 'counter_state_stopgenerator')
    def _project_consumption_generator(self):
        for counter in self:
            if counter.counter_state_stopgenerator == 0:
                counter.project_consumption_generator = False
            else:
                counter.project_consumption_generator = counter.counter_state_stopgenerator - counter.counter_state_startgenerator

    @api.depends('counter_state_starthours', 'counter_state_stophours')
    def _project_consumption_hours(self):
        for counter in self:
            if counter.counter_state_stophours == 0:
                counter.project_consumption_hours = False
            else:
                counter.project_consumption_hours = counter.counter_state_stophours - counter.counter_state_starthours

    @api.depends('counter_state_start', 'counter_state_stop')
    def _project_consumption(self):
        for counter in self:
            if counter.counter_state_stop == 0:
                counter.project_consumption = False
            else:
                counter.project_consumption = counter.counter_state_stop - counter.counter_state_start

    @api.depends('project_id')
    def _compute_project_code(self):
        for counter in self:
            if counter.project_id:
                counter.project_code = counter.project_id.project_code
            else:
                counter.project_code = False


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    consumption_electrical = fields.One2many('energy.counter',
                                             'project_id',
                                             domain=[('counter_type', '=', 'electrical')],
                                             readonly=True,
                                             )
    consumption_water = fields.One2many('energy.counter',
                                        'project_id',
                                        domain=[('counter_type', '=', 'water')],
                                        readonly=True)
    consumption_technical_water = fields.One2many('energy.counter',
                                                  'project_id',
                                                  domain=[('counter_type', '=', 'technical_water')],
                                                  readonly=True)

