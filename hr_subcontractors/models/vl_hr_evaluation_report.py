# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import tools
from odoo import models, fields, api, osv, _


class VLHREvaluationReport(models.Model):
    _name = "vl.hr.evaluation.report"
    _description = "Evaluations Statistics"
    _auto = False
    create_date = fields.Datetime('Create Date', readonly=True),
    delay_date = fields.Float('Delay to Start', digits=(16, 2), readonly=True),
    overpass_delay = fields.Float('Overpassed Deadline', digits=(16, 2), readonly=True),
    deadline = fields.Date("Deadline", readonly=True),
    request_id = fields.Many2one('survey.user_input', 'Request ID', readonly=True),
    closed = fields.Date("Close Date", readonly=True),  # TDE FIXME master: rename into date_close
    plan_id = fields.Many2one('hr_evaluation.plan', 'Plan', readonly=True),
    employee_id = fields.Many2one('hr.employee', "Employee", readonly=True),
    rating = fields.Selection([
            ('0', 'Significantly bellow expectations'),
            ('1', 'Did not meet expectations'),
            ('2', 'Meet expectations'),
            ('3', 'Exceeds expectations'),
            ('4', 'Significantly exceeds expectations'),
        ], "Overall Rating", readonly=True),
    nbr = fields.Integer('# of Requests', readonly=True),  # TDE FIXME master: rename into nbr_requests
    state = fields.Selection([
            ('draft', 'Draft'),
            ('wait', 'Plan In Progress'),
            ('progress', 'Final Validation'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ], 'Status', readonly=True),

    _order = 'create_date desc'

    _depends = {
        'vl.hr.evaluation.interview': ['evaluation_id', 'id', 'request_id'],
        'vl.hr.evaluation': [
            'create_date', 'date', 'date_close', 'employee_id', 'plan_id',
            'rating', 'state',
        ],
    }

    @api.multi
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'vl.hr.evaluation_report')
        cr.execute("""
            create or replace view VLHREvaluationReport as (
                 select
                     min(l.id) as id,
                     s.create_date as create_date,
                     s.employee_id,
                     l.request_id,
                     s.plan_id,
                     s.rating,
                     s.date as deadline,
                     s.date_close as closed,
                     count(l.*) as nbr,
                     s.state,
                     avg(extract('epoch' from age(s.create_date,CURRENT_DATE)))/(3600*24) as  delay_date,
                     avg(extract('epoch' from age(s.date,CURRENT_DATE)))/(3600*24) as overpass_delay
                     from
                 VLHREvaluationInterview l
                LEFT JOIN
                     VLHREvaluation on (s.id=l.evaluation_id)
                 GROUP BY
                     s.create_date,
                     s.state,
                     s.employee_id,
                     s.date,
                     s.date_close,
                     l.request_id,
                     s.rating,
                     s.plan_id
            )
        """)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: