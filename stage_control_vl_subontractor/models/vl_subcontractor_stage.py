# -*- coding: utf-8 -*-
# Copyright © 2017 Decodio d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VLSubcontractorStage(models.Model):
    _name = 'vl.subcontractor.stage'
    _inherit = ['stage.control.common']
    _stage_for_model_name = ['vl.subcontractor']
    _description = "Subcontractor stages"
    _order = 'sequence'

    #def init(self):
    #    """ This hook will set no_update on stage data
    #        so user modifications will be preserved on module upgrade.
    #        see also hooks.py
    #    """
    #    self._cr.execute("""
    #        UPDATE mgmtsystem_audit AS aud
    #           SET stage_id = (SELECT id
    #                             FROM mgmtsystem_audit_stage AS aud_s
    #                            WHERE aud.state=aud_s.state
    #                            ORDER BY sequence ASC
    #                            LIMIT 1)
    #        WHERE stage_id is NULL
    #        """)


class VLSubcontractorAction(models.Model):
    _name = 'vl.subcontractor.audit'
    _inherit = ['model.stage.control.common', 'vl.subcontractor']
    _inherit = 'vl.subcontractor'
    _stage_model_name = 'vl.subcontractor.stage'

    def _get_default_stage_id(self):
        stage_obj = self.env[self._stage_model_name]
        stage = stage_obj.search([], order="sequence asc", limit=1)
        return stage

    stage_id = fields.Many2one('vl.subcontractor.stage', 'Stage',
                default=_get_default_stage_id, track_visibility='onchange',)
    state = fields.Selection(
        related='stage_id.state', store=True, readonly=True)
    # DEPREC task_ids = fields.One2many('project.task', 'mgmtsystem_audit_id', string='Tasks')

    @api.multi
    def button_close(self):
        """When Audit is closed, post a message to followers' chatter."""
        self.message_post(_("Audit closed"))
        subcontractor_stage_obj = self.env['vl.subcontractor.stage']
        closed_stage_id = subcontractor_stage_obj.search([('state', '=', 'done')],
                                      order="sequence asc", limit=1)
        if closed_stage_id:
            return self.write({'stage_id': closed_stage_id.id,
                               'closing_date': fields.Datetime.now()})
        else:
            raise UserError(_("Please create a stage for done Audits!"))