# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _, tools


class LeadReport(models.Model):
    _name = 'lead.report'
    _auto = False  # do NOT create table
    _description = "optional desc"
    _rec_name = 'name'  # if name is not called "name"
    _order = 'create_date DESC'

    name = fields.Char(string='Prilika', readonly=True)
    create_date = fields.Date(string='Kreirano')
    user_id = fields.Many2one(comodel_name='res.users', string='Prodavac')
    country_id = fields.Many2one('res.country', 'Country')
    imo_vat = fields.Char(strig='Imo/VAT')
    dock_stay = fields.Integer('Dock Stay')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'lead_report')
        self._cr.execute("""
            CREATE OR REPLACE VIEW lead_report AS 
                SELECT cl.id
                      ,cl.name
                      ,cast(cl.create_date as date) create_date
                      ,cl.user_id , rp.country_id
                      ,coalesce(rp.imo, rp.vat, 'N/A') imo_vat
                      ,cl.dock_stay
                 FROM crm_lead as cl
                 JOIN res_partner as rp ON rp.id = cl.partner_id  
            """)
