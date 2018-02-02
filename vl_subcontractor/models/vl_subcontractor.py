# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class VlSubcontractor(models.Model):
    _name = 'vl.subcontractor'
    _description = "Subcontractor"
    _order = "priority desc, id desc"
    _inherit = ['mail.thread', 'ir.need action_mixin', 'utm.mixin']
    _mail_mass_mailing = _('Applicants')

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name')
    phone = fields.Integer(string='Phone')
    country_id = fields.Many2one('res.country', 'Country')
    birthday = fields.Date(strig='Birthday')

    name = fields.Char("Subject / Applicant name", required=True)
    active = fields.Boolean("Active", default=True,
                            help="If the active field is set to false, it will allow you "
                                 "to hide the case without removing it.")
    details = fields.Text()
    state = fields.Selection(
        selection=[('draft', 'Todo'), ('done', 'Done')],
        string='Status',
        required=True,
        readonly=True,
        default="draft",
    )
    address = fields.Text("Address")
    per_id_number = fields.Char("Personal identification number")
    email_from = fields.Char("General Email address", help="These people will receive email.")
    partner_phone = fields.Char("Telephone")
    fax_number = fields.Char("Fax Number")
    contact_person = fields.Char("Contact Person / Title")
    contact_person_email = fields.Char("Contact Person Email)", help="This person will be contacted for additional info")
    filled_in_by = fields.Char("Application filled in by / Title")
    financial_group = fields.Text("Financial Group/ Owners")
    company_age = fields.Integer("Company age")
    product_range = fields.Text("Product range")
    type_service = fields.Text("Type of service")
    bank = fields.Text("Bank")
    bank_account = fields.Char("Bank account")
    total_personnel = fields.Integer("Total personnel")
    pipe_welders = fields.Integer("Pipe welders")
    administration = fields.Integer("Administration")
    ship_fitter = fields.Integer("Ship fitters")
    management = fields.Integer("Management")
    locksmith  = fields.Integer("Locksmith")
    manpower = fields.Integer("Manpower")
    mechanic  = fields.Integer("Mechanic")
    foreman  = fields.Integer("Foreman")
    electrician  = fields.Integer("Electricina")
    welders  = fields.Integer("Welders")
    other  = fields.Integer("Other")
    proj1_company = fields.Char("Company name")
    proj1_address = fields.Char("Address")
    proj1_manager_name = fields.Char("Project manager")
    proj1_project  = fields.Char("Bank account")
    proj1_date = fields.Date("Project date")
    proj1_project_desc = fields.Text("Short project description")
    proj2_company = fields.Char("Company name")
    proj2_address = fields.Char("Address")
    proj2_manager_name = fields.Char("Project manager")
    proj2_project = fields.Char("Bank account")
    proj2_date = fields.Date("Project date")
    proj2_project_desc = fields.Text("Short project description")
    proj3_company = fields.Char("Company name")
    proj3_address = fields.Char("Address")
    proj3_manager_name = fields.Char("Project manager")
    proj3_project = fields.Char("Bank account")
    proj3_date = fields.Date("Project date")
    proj3_project_desc = fields.Text("Short project description")
    qa_system = fields.Char("QA System")
    qa_contact = fields.Char("QA System Contact")
    qa_organization = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA System Contact',
        required=True,
        default="No")
    qa_contract_rev = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Contract review',
        required=True,
        default="No")
    qa_engineering = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Engineering',
        required=True,
        default="No")
    qa_docs = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Documentation',
        required=True,
        default="No")
    qa_purchasing = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Purchasing',
        required=True,
        default="No")
    qa_trace_material = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Traceability of Materials',
        required=True,
        default="No")
    qa_spec_proces = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Special Processes',
        required=True,
        default="No")
    qa_inspect_test = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Inspection/Testing',
        required=True,
        default="No")
    qa_calibration = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Calibration',
        required=True,
        default="No")
    qa_non_conf_ite = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Non conforming Items',
        required=True,
        default="No")
    qa_correct_action = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Corrective Actions',
        required=True,
        default="No")
    qa_handle_stor_pack = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Handeling/Stroge/Packing',
        required=True,
        default="No")
    qa_qal_rec = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Quality Records',
        required=True,
        default="No")
    qa_auditors = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Auditors',
        required=True,
        default="No")
    qa_safe_manage = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Standard of Safety Management',
        required=True,
        default="No")
    qa_sys = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA System',
        required=True,
        default="No")
    qa_acc_inc_stat = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Accident/Incident Statistics',
        required=True,
        default="No")
    agent_shipp_agent = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Shipping agent',
        required=True,
        default="No")

    description = fields.Text("Description")