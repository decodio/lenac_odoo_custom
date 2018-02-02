# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class ResPhonebook(models.Model):
    _name = 'res.phonebook'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name')
    phone = fields.Integer(string='Phone')
    country_id = fields.Many2one('res.country', 'Country')
    birthday = fields.Date(strig='Birthday')