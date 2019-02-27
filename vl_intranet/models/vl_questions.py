# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, _


class WebsitePortalQuestion(models.Model):
    _name = 'website.portal.question'
    _inherit = ['mail.thread', 'ir.needaction_mixin', 'utm.mixin']
    _mail_mass_mailing = _('Applicants')

    name = fields.Char('Name', required=True)
    email = fields.Char('Email', required=True)
    mobile = fields.Char('Phone')
    question = fields.Text('Question', help='Write your article here', required=True)

    article_author = fields.Many2one(
        'res.users',
        string='Author',
        index=True,
        track_visibility='onchange',
        required=True,
        default=lambda self: self.env.uid,
        readonly=True
    )

