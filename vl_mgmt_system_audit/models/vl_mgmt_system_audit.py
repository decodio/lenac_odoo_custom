# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class MgmtsystemAudit(models.Model):

    _inherit = ['mgmtsystem.audit']

    system_ids = fields.Many2many('mgmtsystem.system', 'System')

    @api.model
    def _fill_system(self):
        system = self.env['mgmtsystem.system'].search(
            ['&', ('system_id', '!=', False), ('system_ids', '=', False)])
        for record in system:
            if not record.system_ids and record.system_id:
                record.system_ids = [(4, record.system_id.id)]
            else:
                record.system_ids = False


class MgmtsystemVerificationLine(models.Model):
    """Class to manage verification's Line."""
    _inherit = "mgmtsystem.verification.line"

    name_id = fields.Many2one('mgmtsystem.system')

    @api.onchange('name_id')
    def _onchange_name_id(self):
        self.name = self.name_id.name




