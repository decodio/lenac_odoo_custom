# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2017 Decodio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class HrJobApprovalRejectReason(models.Model):
    _name = 'hr.job.approval.reject.reason'
    _inherit = ['approval.reject.reason.common']
    _description = 'Job Description Approval Reject Reason'


class HrJobApprovalRejectReasonWizard(models.TransientModel):
    _name = 'hr.job.approval.reject.reason.wizard'
    _inherit = ['approval.reject.reason.wizard.common']
    _description = 'Job Description Approval Reject Reason Wizard'

    approval_reject_reason_id = fields.Many2one(
        'hr.job.approval.reject.reason',
        'Reject Reason',
        required=True
    )

    @api.onchange('approval_reject_reason_id')
    def onchange_stage_probability(self):
        self.comment = self.approval_reject_reason_id.comment

    @api.multi
    def reject_with_reason(self):
        res = super(HrJobApprovalRejectReasonWizard, self).reject_with_reason()

        if self._context.get('active_ids') and self._context.get(
                'active_model'):
            active_ids = self._context['active_ids']
            active_model = self._context['active_model']
            model = self.env[active_model]
        if active_ids and active_model:
            jobs = model.browse(active_ids)
            for job in jobs:
                approval_reject_reason_id = self.approval_reject_reason_id and\
                                            self.approval_reject_reason_id.id or False
                comment = self.comment or ''
                active_stage_id = self._context.get('active_stage_id')
                active_stage = self.env['hr.job.long.stage'].browse([active_stage_id])
                if active_stage and active_stage.rejected_mail_template_id:
                    rejected_msg = comment
                    job.with_context(self._context,
                                          rejected_msg=rejected_msg).send_mail(
                        active_stage.rejected_mail_template_id,
                        job.id)
        return res
