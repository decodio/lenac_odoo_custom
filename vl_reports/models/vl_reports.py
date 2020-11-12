# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class MgmtsystemAudit(models.Model):

    _inherit = ['mgmtsystem.audit']

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


class MgmtsystemNonconformity(models.Model):

    _inherit = ['mgmtsystem.nonconformity']

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