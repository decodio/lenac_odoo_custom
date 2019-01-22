# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.website.models.website import slug
from odoo.http import request


# NB: DO NOT FORWARD PORT THE FALSY LEAVES IN 11.0
class WebsiteVlEmployee(http.Controller):

    @http.route('/my/phonebook', type='http', auth="user", website=True)
    def render_phonebook(self, **kwargs):
        departments = http.request.env['hr.department'].sudo().search([])
        employees = http.request.env['hr.employee'].sudo().search([])
        return http.request.render('vl_hr.vl_phonebook', {
            'departments': departments,
            'employees': employees
        })
