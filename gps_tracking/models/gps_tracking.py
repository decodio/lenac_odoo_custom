# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class GpsCard(models.Model):
    _name = 'gps.card'

    card_no=fields.char(string='Card number')
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')


class GpsLocationHistory(models.Model):
    _name = 'gps.location.history'

    latitude = fields.Float(string='Lat', digits=(16, 5))
    longitude = fields.Float(string='Long', digits=(16, 5))
    vehicle_inv_no = fields.Char( string='Vehicle Invertory Number')
    card_no = fields.Many2one('gps.card', string='Badge')
    is_active = fields.Boolean(string='Active', default=False)
    battery_voltage = fields.Float(String='Battery voltage')
