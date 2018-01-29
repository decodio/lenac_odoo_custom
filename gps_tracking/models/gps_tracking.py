# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class GpsLocationHistory(models.Model):
    _name = 'gps.location.history'

    latitude = fields.Float(string='Lat',digits=(16,5))
    longitude = fields.Float(string='Long',digits=(16,5))
    vehicle_id = fields.Many2one('gps.vehicle', 'Country')
    birthday = fields.Date(strig='Birthday')