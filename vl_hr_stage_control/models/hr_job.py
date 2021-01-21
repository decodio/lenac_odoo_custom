# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrJobApproval(models.Model):
    _name = 'hr.job.approval'
    _inherit = ['document.approval.common']

    _sql_constraints = [
        ('sequence_uniq', 'UNIQUE(sequence, document_id)',
         'The sequence number must be unique by job')
    ]

    document_id = fields.Many2one('hr.job.long', string='Job')


class HrJobApprovalHistory(models.Model):
    _name = 'hr.job.approval.history'
    _inherit = ['approval.history.common']

    job_long_id = fields.Many2one('hr.job.long', 'Job description')
    stage_id = fields.Many2one(
        comodel_name='hr.job.long.stage',
        string='Job Stage')
    approval_reject_reason_id = fields.Many2one(
        'hr.job.approval.reject.reason',
        'Reject Reason',
        readonly=True
    )
    version = fields.Text(  # TODO: required=True
        string="Version", readonly=True, default='0.0',
        help="Next version")


class HrJobLong(models.Model):
    _name = 'hr.job.long'
    _description = "Job Position Description"
    _inherit = ['model.stage.control.common', 'hr.job.long']
    _stage_model_name = 'hr.job.long.stage'

    """APPROVAL"""
    approver_id = fields.Many2one(copy=False)

    def _get_default_stage_id(self):
        stage_obj = self.env['hr.job.long.stage']
        # from category
        stage = stage_obj.search([], order="sequence asc", limit=1)
        return stage

    stage_id = fields.Many2one(
        'hr.job.long.stage',
        'Stage',
        default=_get_default_stage_id,
        track_visibility='onchange',
        copy=False, order='sequence'  # , TODO: required=True
    )
    state = fields.Selection(
        related='stage_id.state', store=True, readonly=True)

    next_version = fields.Text(
        string="Next Version", default='1.0', required=True,
        readonly=True)

    version = fields.Text(
        string="Version", readonly=True, default='0.0')

    stage_approval_id = fields.Many2one(
        comodel_name='hr.job.stage.approval',
        string='Current stage approval line',
        readonly=True)

    document_approval_id = fields.Many2one(
        comodel_name='hr.job.approval',
        string='Current document approval line',
        readonly=True)

    approval_ids = fields.One2many(
        'hr.job.approval',
        'document_id',
        string='Approvals')

    approval_history_ids = fields.One2many(
        'hr.job.approval.history',
        'job_long_id', string='Approvals history')

    @api.multi
    def write(self, vals):
        for document in self:
            if vals.get('stage_id'):
                old_stage = document.stage_id
                new_stage = self.env[self._stage_model_name].browse(
                    vals.get('stage_id'))
                self._check_approver_id(old_stage, new_stage)

                next_approval_vals = document.get_next_approval_vals(new_stage)
                vals.update(next_approval_vals)
                # send mail
                # add reading history date nov state not read
                # recipient_emails
                # document_link_url

                # get first approval line or write false
                # in approver_id and approval_id fields

                if vals.get('stage_id'):
                    if new_stage.approvers_mail_template_id and next_approval_vals.get('approver_id'):
                        approver_id = self.env['res.users'].browse([next_approval_vals.get('approver_id')])
                        if approver_id:
                            recipient_approver_id = approver_id.partner_id.id
                            self.with_context(self._context,
                                              recipient_approver_id=recipient_approver_id).send_mail(
                                new_stage.approvers_mail_template_id, self.id)
        res = super(HrJobLong, self).write(vals)
        return res

    @api.multi
    def _check_approver_id(self, old_stage, new_stage):
        if new_stage.sequence > old_stage.sequence:
            if self.approver_id:
                raise ValidationError(
                    _('Error ! You can not proceede to next stage.'
                      'User %s must approve document') % (self.approver_id.name,))
        return True

    @api.multi
    def mark_rejected(self, action_name=False):
        action_name = 'vl_hr_stage_control.action_hr_job_approval_reject_reason'
        action = super(HrJobLong, self).mark_rejected(action_name)
        if action:
            if not action.get('context'):
                action['context'] = {}
            action['context'] = {'active_stage_id': self.stage_id.id}
        return action

    @api.multi
    def mark_approved(self):
        super(HrJobLong, self).mark_approved()
        if self.stage_id.approvers_mail_template_id and self.approver_id:
            recipient_approver_id = self.approver_id.partner_id.id
            self.with_context(self._context,
                              recipient_approver_id=recipient_approver_id).send_mail(
                self.stage_id.approvers_mail_template_id, self.id)
