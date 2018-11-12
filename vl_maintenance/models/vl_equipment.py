# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class VLMaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

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

    pc_number = fields.Char('Inventory number')
    #installed_os = fields.Selection(
    #   selection=[('winxp', 'Windows XP'), ('win7', 'Windows 7'), ('win10', 'Windows 10'),
    #              ('winser2003', 'Windows Server 2003'), ('winser2008', 'Windows Server 2008'),
    #              ('winser2008R2', 'Windows Server 2008 R2'), ('winser2012', 'Windows Server 2012'),
    #              ('winser2012R2', 'Windows Server 2012 R2')],
    #   string='Installed OS',
    #   required=False)
    installed_os = fields.Many2one('allowed.os', string='Installed OS')
    installed_sw = fields.Many2many('allowed.os', string='Installed software')
    date_purchased = fields.Date('Date of purchase')
    ndep_number = fields.Char('Department number')
    nemp_number = fields.Char('Assigned employee number')
    old_employee_id = fields.Many2one('hr.employee', string='Assigned to Employee', track_visibility='onchange')
    old_department_id = fields.Many2one('hr.department', string='Assigned to Department', track_visibility='onchange')
    old_equipment_assign_to = fields.Selection(
        [('department', 'Department'), ('employee', 'Employee'), ('other', 'Other')],
        string='Used By',
        required=True,
        default='employee')
    emp_number = fields.Char('Employee number')
    dep_number = fields.Char('Department number')
    date_assigned = fields.Date('Date assigned')
    n_location = fields.Char('Assigned location')


class AllowedSoftware(models.Model):
    _name = 'allowed.os'
    _description = 'Installed software'

    name = fields.Char(string="Software name", required='True')
    sw_vendor = fields.Char(string="Software vendor")
    sw_version = fields.Char(string="Software version")
    sw_licence = fields.Selection(selection=[('free', 'Free'), ('personal', 'Personal use'),
                                             ('spaid', 'Single paid licence'), ('mpaid', 'Multiple activation key'),
                                             ('subs', 'Subscription')],
                                  string='Licence type',
                                  required=False)
    sw_serial = fields.Char(string="Serial key")
    sw_purchase_date = fields.Date(string="Date of purchase")
    sw_licence_exp = fields.Date(string="Expiration date")
    sw_price = fields.Integer(string="Licence cost")
    sw_licence_assignd_person = fields.Many2one('hr.employee', string='Assigned to Employee')
    sw_licence_assignd_dep = fields.Many2one('hr.department', string='Assigned to Department')
    sw_spec = fields.Selection(selection=[('def', 'Installed by default'),
                                          ('dep_spec', 'Department specific')],
                               string='Installation type',
                               required='True')
    sw_type = fields.Selection(selection=[('prog', 'Program'), ('OS', 'Operating system')],
                               string='Software type',
                               required='True')