# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EnergyCounter(models.Model):
    _name = 'energy.counter'

    project_id = fields.Many2one('crm.lead')
    project_code = fields.Integer('crm.lead', compute='_compute_project_code', readonly=True, store=True)
    counter_location = fields.Many2one('resource.dock')
    date_write_start = fields.Datetime(default=lambda self: fields.datetime.now())
    date_write_stop = fields.Datetime(default=lambda self: fields.datetime.now())
    date_write_monthend = fields.Datetime(default=lambda self: fields.datetime.now())
    counter_state_start = fields.Integer('Enter the value of the counter on connect')
    counter_state_stop = fields.Integer('Enter the value of the counter on disconnect')
    counter_state_monthend = fields.Integer('Enter the value of the counter on the end of the month')

    @api.depends('project_id')
    def _compute_project_code(self):
        for counter in self:
            if counter.project_id:
                counter.project_code = counter.project_id.project_code
            else:
                counter.project_code = False



    #counter_type = fields.Selection([('energy', 'Energy counter'), ('water', 'Water counter')],
    #                                     string='Sort of equipment',
    #                                     required=True)




