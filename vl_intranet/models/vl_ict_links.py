# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, _

class WebsiteIctLinks(models.Model):
    _name = 'website.ict.links'

    name = fields.Char('Link name')
