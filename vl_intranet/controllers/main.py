# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import http, _
from odoo.addons.website_portal.controllers.main import website_account
from odoo.http import request


class WebsiteAccount(website_account):

    _items_per_page_news = 5

    def _prepare_portal_layout_values(self):
        values = super(WebsiteAccount, self)._prepare_portal_layout_values()
        #article Viktor Lenac
        article = http.request.env['website.portal.article'].sudo().search([])
        #article Syindicate
        #article2 = http.request.env['website.portal.asyndicate'].sudo().search([])
        #article Viktor Servisi
        article3 = http.request.env['website.portal.vs'].sudo().search([])
        #links for various applications
        ictlinks = http.request.env['website.ict.links'].sudo().search([])

        values.update({
            'article': article,
            #'article2': article2,
            'ictlinks': ictlinks,
        })
        return values

    @http.route(['/my/news', '/my/news/page/<int:page>'], type='http', auth="user", website=True)
    def render_news(self, page=1, date_begin=None, date_end=None, sortby=None, **kwargs):
        values = self._prepare_portal_layout_values()

        sortings = {
            'date': {'label': _('Newest'), 'order': 'article_date desc'},
            'date_a': {'label': _('Oldest'), 'order': 'article_date asc'}
        }

        order = sortings.get(sortby, sortings['date'])['order']

        article_count = request.env['website.portal.article'].search_count([('website_published', '=', True)])
        archive_groups = self._get_archive_groups('website.portal.article')

        pager = request.website.pager(
            url="/my/news",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=article_count,
            page=page,
            step=self._items_per_page_news
        )

        article = http.request.env['website.portal.article'].sudo().search([('website_published', '=', True)],
                                                                           order=order,
                                                                           limit=self._items_per_page_news,
                                                                           offset=pager['offset'])

        values.update({'article_count': article_count,
                       'date': date_begin,
                       'date_end': date_end,
                       'article': article,
                       'sortings': sortings,
                       'archive_groups': archive_groups,
                       'default_url': '/my/news',
                       'pager': pager
                       })

        return http.request.render('vl_intranet.vl_article', values, {
        })
    """ Working but not in use
    @http.route(['/my/syndicate', '/my/syndicate/page/<int:page>'], type='http', auth="user", website=True)
    def render_news2(self, page=1, date_begin=None, date_end=None, sortby=None, **kwargs):
        values = self._prepare_portal_layout_values()

        sortings = {
            'date': {'label': _('Newest'), 'order': 'article_date desc'},
            'date_a': {'label': _('Oldest'), 'order': 'article_date asc'}
        }

        order = sortings.get(sortby, sortings['date'])['order']

        article_count = request.env['website.portal.asyndicate'].search_count([('website_published', '=', True)])
        archive_groups = self._get_archive_groups('website.portal.asyndicate')

        pager = request.website.pager(
            url="/my/syndicate",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=article_count,
            page=page,
            step=self._items_per_page_news
        )

        article2 = http.request.env['website.portal.asyndicate'].sudo().search([('website_published', '=', True)],
                                                                           order=order,
                                                                           limit=self._items_per_page_news,
                                                                           offset=pager['offset'])

        values.update({'article_count': article_count,
                       'date': date_begin,
                       'date_end': date_end,
                       'article2': article2,
                       'sortings': sortings,
                       'archive_groups': archive_groups,
                       'default_url': '/my/syndicate',
                       'pager': pager
                       })

        return http.request.render('vl_intranet.vl_asyndicate', values, {
        })
    """
    @http.route(['/my/viktorservisi', '/my/viktorservisi/page/<int:page>'], type='http', auth="user", website=True)
    def render_news3(self, page=1, date_begin=None, date_end=None, sortby=None, **kwargs):
        values = self._prepare_portal_layout_values()

        sortings = {
            'date': {'label': _('Newest'), 'order': 'article_date desc'},
            'date_a': {'label': _('Oldest'), 'order': 'article_date asc'}
        }

        order = sortings.get(sortby, sortings['date'])['order']

        article_count = request.env['website.portal.vs'].search_count([('website_published', '=', True)])
        archive_groups = self._get_archive_groups('website.portal.vs')

        pager = request.website.pager(
            url="/my/syndicate",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=article_count,
            page=page,
            step=self._items_per_page_news
        )

        article3 = http.request.env['website.portal.vs'].sudo().search([('website_published', '=', True)],
                                                                               order=order,
                                                                               limit=self._items_per_page_news,
                                                                               offset=pager['offset'])

        values.update({'article_count': article_count,
                       'date': date_begin,
                       'date_end': date_end,
                       'article3': article3,
                       'sortings': sortings,
                       'archive_groups': archive_groups,
                       'default_url': '/my/viktorservisi',
                       'pager': pager
                       })

        return http.request.render('vl_intranet.vl_viktor_servisi', values, {
        })

    """ TO DO
    @http.route(['/my/questions', '/my/ictlinks/page/<int:page>'], type='http', auth="public", website=True)
    def render_questions(self, **kwargs):
        values = self._prepare_portal_layout_values()

        values.update({
            'default_url': '/my/questions'
        })

        error = {}
        default = {}
        if 'vl_questions_error' in request.session:
            error = request.session.pop('vl_questions_error')
            default = request.session.pop('vl_questions_default')

        return http.request.render('vl_intranet.vl_questions', values, {
            'error': error,
            'default': default,
        })
    """

    @http.route(['/my/itclinks', '/my/ictlinks/page/<int:page>'], type='http', auth="user", website=True)
    def render_ict_links(self, **kwargs):
        values = self._prepare_portal_layout_values()

        values.update({
            'default_url': '/my/ictlinks'
        })

        return http.request.render('vl_intranet.vl_itclinks', values, {
        })


