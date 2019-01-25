# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http, _
from odoo.addons.website.models.website import slug
from odoo.http import request


# NB: DO NOT FORWARD PORT THE FALSY LEAVES IN 11.0
class WebsiteVlSubcontractor(http.Controller):

    @http.route('/vl_subcontractor', type='http', auth="public", website=True)
    def subc_apply(self, **kwargs):
        error = {}
        default = {}
        if 'vl_subcontractor_error' in request.session:
            error = request.session.pop('vl_subcontractor_error')
            default = request.session.pop('vl_subcontractor_default')
        return request.render("vl_subcontractor.vl_subcontractor", {
            'error': error,
            'default': default,
        })