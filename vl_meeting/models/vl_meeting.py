# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
import logging
_logger = logging.getLogger(__name__)


class Attendee(models.Model):
    _inherit = 'calendar.attendee'


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
                meeting.attendee_ids._send_mail_to_attendees('vl_meeting.notes_of_meeting')
        return True
