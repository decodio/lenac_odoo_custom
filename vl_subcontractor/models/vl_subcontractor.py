# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Viktor Lenac
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class VlSubcontractor(models.Model):
    _name = 'vl.subcontractor'
    _description = "Subcontractor"
    #_order = "priority desc, id desc"
    _inherit = ['mail.thread', 'ir.needaction_mixin', 'utm.mixin']
    _mail_mass_mailing = _('Applicants')

    survey_id = fields.Many2one('survey.survey', string="Survey")
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null", oldname="response")
    #partner_id =

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

    address_street = fields.Text("Company Address")
    address_po_box = fields.Text("PO Box")
    address_city = fields.Text("City")
    address_country = fields.Many2one('res.country', 'Country')
    per_id_number = fields.Char("Personal identification number")
    email_from = fields.Char(
        "General Email address",
        help="These people will receive email.")
    partner_phone = fields.Char("Telephone")
    fax_number = fields.Char("Fax Number")
    contact_person = fields.Char("Contact Person / Title")
    contact_person_email = fields.Char(
        "Contact Person Email)",
        help="This person will be contacted for additional info")
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
    locksmith = fields.Integer("Locksmith")
    manpower = fields.Integer("Manpower")
    mechanic = fields.Integer("Mechanic")
    foreman = fields.Integer("Foreman")
    electrician = fields.Integer("Electricina")
    welders = fields.Integer("Welders")
    other = fields.Integer("Other")
    proj1_company = fields.Char("Company name")
    proj1_address = fields.Char("Address")
    proj1_manager_name = fields.Char("Project manager")
    proj1_date = fields.Date("Project date")
    proj1_project_desc = fields.Text("Short project description")
    proj2_company = fields.Char("Company name")
    proj2_address = fields.Char("Address")
    proj2_manager_name = fields.Char("Project manager")
    proj2_date = fields.Date("Project date")
    proj2_project_desc = fields.Text("Short project description")
    proj3_company = fields.Char("Company name")
    proj3_address = fields.Char("Address")
    proj3_manager_name = fields.Char("Project manager")
    proj3_date = fields.Date("Project date")
    proj3_project_desc = fields.Text("Short project description")
    contact_qms = fields.Char("QA System Contact")
    qa_system_9000 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='ISO 9001 Standard',
        required=True,
        default="no")
    qa_organization = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Organization',
        required=True,
        default="no")
    qa_contract_rev = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Contract review',
        required=True,
        default="no")
    qa_engineering = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Engineering',
        required=True,
        default="no")
    qa_docs = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Documentation',
        required=True,
        default="no")
    qa_purchasing = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Purchasing',
        required=True,
        default="no")
    qa_trace_material = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Traceability of Materials',
        required=True,
        default="no")
    qa_spec_proces = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Special Processes',
        required=True,
        default="no")
    qa_inspect_test = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Inspection/Testing',
        required=True,
        default="no")
    qa_calibration = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Calibration',
        required=True,
        default="no")
    qa_non_conf_ite = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Non conforming Items',
        required=True,
        default="no")
    qa_correct_action = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Corrective Actions',
        required=True,
        default="no")
    qa_handle_stor_pack = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Handeling/Stroge/Packing',
        required=True,
        default="no")
    qa_qal_rec = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Quality Records',
        required=True,
        default="no")
    qa_auditors = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='QA Auditors',
        required=True,
        default="no")
    qa_system_14000 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='ISO 14001 Standard',
        required=True,
        default="no")
    qa_policy_14 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Policy',
        required=True,
        default="no")
    qa_waste_mgmt_14 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Waste management',
        required=True,
        default="no")
    qa_dan_haz_sub_14 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Control of dangerous and hazardous substances',
        required=True,
        default="no")
    qa_acc_inc_stat_14 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Acident/Incident Statistics',
        required=True,
        default="no")
    qa_system_18000 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='ISO 18001 Standard',
        required=True,
        default="no")
    qa_policy_18 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Policy',
        required=True,
        default="no")
    qa_mach_main_18 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Machinery maintainance',
        required=True,
        default="no")
    qa_acc_inc_stat_18 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Acident/Incident Statistics',
        required=True,
        default="no")
    qa_system_50000 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='ISO 50001 Standard',
        required=True,
        default="no")
    qa_policy_50 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Policy',
        required=True,
        default="no")
    qa_eng_track_type_50 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Energy consumption tracking by energy type',
        required=True,
        default="no")
    qa_mgmt_goal_50 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Energy management goals',
        required=True,
        default="no")
    qa_action_plan_50 = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Action plans for energy savings',
        required=True,
        default="no")
    agent = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Agent',
        required=True,
        default="no")
    agent_ship_agent = fields.Selection(
        selection=[('yes', 'Yes'), ('no', 'No')],
        string='Shipping agent',
        required=True,
        default="no")

    description = fields.Text("Description")

    @api.multi
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create(
                {'survey_id': self.survey_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()