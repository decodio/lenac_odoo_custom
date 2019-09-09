# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, _
import logging
_logger = logging.getLogger(__name__)


class Attendee(models.Model):
    _inherit = 'calendar.attendee'

    @api.multi
    def _send_mail_to_attendeess(self, template_xmlid, force_send=False):
        res = False

        if self.env['ir.config_parameter'].get_param('calendar.block_mail') or self._context.get(
                "no_mail_to_attendees"):
            return res

        calendar_view = self.env.ref('calendar.view_calendar_event_calendar')
        invitation_template = self.env.ref(template_xmlid)

        # ics_files = self.mapped('event_id').get_ics_file()

        colors = {
            'needsAction': 'grey',
            'accepted': 'green',
            'tentative': '#FFFF00',
            'declined': 'red'
        }
        rendering_context = dict(self._context)
        rendering_context.update({
            'color': colors,
            'action_id': self.env['ir.actions.act_window'].search([('view_id', '=', calendar_view.id)], limit=1).id,
            'dbname': self._cr.dbname,
            'base_url': self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069')
        })
        invitation_template = invitation_template.with_context(rendering_context)

        mails_to_send = self.env['mail.mail']
        for attendee in self:
            if attendee.email or attendee.partner_id.email:
                # ics_file = ics_files.get(attendee.event_id.id)
                mail_id = invitation_template.send_mail(attendee.id)

                vals = {}
                # if ics_file:
                #    vals['attachment_ids'] = [(0, 0, {'name': 'invitation.ics',
                #                                      'datas_fname': 'invitation.ics',
                #                                      'datas': str(ics_file).encode('base64')})]
                vals['model'] = None
                vals['res_id'] = False
                current_mail = self.env['mail.mail'].browse(mail_id)
                current_mail.mail_message_id.write(vals)
                mails_to_send |= current_mail

        if force_send and mails_to_send:

            res = mails_to_send.send()

        return res


class Meeting(models.Model):
    _inherit = 'calendar.event'
    _description = "Event"

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('report.external_layout')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('report.external_layout', docargs)

    meeting_notes = fields.Text('Meeting conclusion')


    @api.multi
    def action_sendmail(self):
        email = self.env.user.email
        if email:
            for meeting in self:
                meeting.attendee_ids._send_mail_to_attendeess('vl_meeting.notes_of_meeting')
        return True
