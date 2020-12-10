# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class MgmtsystemNonconformity(models.Model):

    _inherit =['mgmtsystem.nonconformity']

    correction = fields.Text('Correction')

