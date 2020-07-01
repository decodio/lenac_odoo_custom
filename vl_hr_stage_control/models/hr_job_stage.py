# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrJobStageApproval(models.Model):
    _name = 'hr.job.stage.approval'
    _inherit = ['stage.approval.common']
    _approval_for_model_name = ['hr.job.long']

    _sql_constraints = [
        ('sequence_uniq', 'UNIQUE(sequence, stage_id)',
         'The sequence number must be unique by stage')
    ]

    stage_id = fields.Many2one('hr.job.long.stage', string='Stage')


class HrJobLongStage(models.Model):
    _name = 'hr.job.long.stage'
    _description = 'Job Long Stage'
    _inherit = ['stage.control.common']
    _stage_for_model_name = ['hr.job.long']

    approval_ids = fields.One2many(
        'hr.job.stage.approval',
        'stage_id',
        string='Approvals')

    approvers_mail_template_id = fields.Many2one(
        comodel_name='mail.template',
        string='Approvers Email Template',
        ondelete='set null',
        domain=lambda self: [('model', 'in', self._stage_for_model_name)],
        help="""This will be sent on document approval to the next document
                    approver.""")

    rejected_mail_template_id = fields.Many2one(
        comodel_name='mail.template',
        string='Rejected Email Template',
        ondelete='set null',
        domain=lambda self: [('model', 'in', self._stage_for_model_name)],
        help="""This will be sent on document reject to the document editor.""")
