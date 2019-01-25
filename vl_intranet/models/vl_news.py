# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, _


#class WebsitePortalNews (models.Model):
#    _name = 'website.portal.news'

#    name = fields.Char('Title')
#    portal_articles = fields.Many2one('website.portal.article')


class WebsitePortalArticle(models.Model):
    _name = 'website.portal.article'
    _inherit = 'website.published.mixin'

    name = fields.Char('Article title', help='Name your article', required=True)
    article_text = fields.Html('Article', help='Write your article here')
    article_date = fields.Datetime(default=lambda self: fields.datetime.now())
    article_author = fields.Many2one(
        'res.users',
        string='Author',
        index=True,
        track_visibility='onchange',
        required=True,
        default=lambda self: self.env.uid,
        readonly=True
    )

    website_published = fields.Boolean(default=False)
