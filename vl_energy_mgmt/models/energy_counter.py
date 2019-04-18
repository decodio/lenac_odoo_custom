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
    counter_state_stop = fields.Integer('Enter the value of the counter on disconnect the month')
    project_consumption = fields.Integer(compute='_project_consumption', readonly=True, store=True)

    counter_type = fields.Selection([('electrical', 'Electrical'),
                                    ('water', 'Water'),
                                    ('technical_water', 'Technical Water')],
                                     string='Meter type',
                                     required=True,
                                     default='electrical')

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


    #counter_type = fields.Selection([('energy', 'Energy counter'), ('water', 'Water counter')],
    #                                     string='Sort of equipment',
    #                                     required=True)




