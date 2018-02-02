# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _, tools


class LeadReport1(models.Model):
    _name = 'lead.report1'
    _auto = False  # do NOT create table
    _description = "optional desc"
    _rec_name = 'name'  # if name is not called "name"
    _order = 'create_date DESC'

    project_code = fields.Integer(string='Radni nalog')
    name = fields.Char(string='Prilika', readonly=True)
    create_date = fields.Date(string='Kreirano')
    user_id = fields.Many2one(comodel_name='res.users', string='Prodavac')
    country_id = fields.Many2one('res.country', 'Country')
    imo_vat = fields.Char(strig='Imo/VAT')
    dock_stay = fields.Integer('Dock Stay')
    lost = fields.Char('Prilika izgubljena')
    lost_description = fields.Char('Razlog gubitka prilike')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'lead_report1')
        self._cr.execute("""
            CREATE OR REPLACE VIEW lead_report1 AS 
                SELECT cl.id,
                    cl.project_code,
                    cl.name,
                    cl.stage_id,
                    to_char(cl.create_date, 'dd.mm.yy'),
                    cl.user_id,
                    rp.country_id,
                    COALESCE(rp.imo, rp.vat, 'N/A'::character varying) AS imo_vat,
                    cl.dock_stay,
                        CASE 
                            WHEN cl.lost_reason_id IS NULL then 'No'
                            WHEN cl.lost_reason_id IS NOT NULL THEN 'Yes'
                            ELSE 'Maybe'
                        END
                        AS LOST	,
                    cl.lost_description,
                    ll.lead_id
                    FROM crm_lead cl		
                    LEFT OUTER JOIN res_partner as rp ON rp.id = cl.partner_id
                    LEFT OUTER JOIN crm_lead_lost as ll on ll.lead_id = cl.id
                    LEFT OUTER JOIN crm_lost_reason as lr on lr.id = ll.id
            """)
