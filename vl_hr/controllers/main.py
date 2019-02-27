# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import http, _
from odoo.addons.website_portal.controllers.main import website_account
from odoo.http import request


#class WebsiteVlEmployee(http.Controller):
class WebsiteAccount(website_account):

    def _prepare_portal_layout_values(self):
        values = super(WebsiteAccount, self)._prepare_portal_layout_values()
        departments = http.request.env['hr.department'].sudo().search([])
        employees = http.request.env['hr.employee'].sudo().search([])
        values.update({
            'departments': departments,
            'employees': employees
        })
        return values

    @http.route(['/my/phonebook', '/my/phonebook/page/<int:page>'], type='http', auth="user", website=True)
    def render_phonebook(self, **kwargs):
        values = self._prepare_portal_layout_values()
        departments = http.request.env['hr.department'].sudo().search([('website_published', '=', True)])
        employees = http.request.env['hr.employee'].sudo().search([])

        values.update({'departments': departments,
                       'employees': employees})

        return http.request.render('vl_hr.vl_phonebook', values, {
        })
