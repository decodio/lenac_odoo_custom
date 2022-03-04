# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
from odoo import api, models, fields, _
#from odoo.addons.cmis_field import fields as cmis_fields


class OwnerEquipmentProject(models.Model):
    _name = 'owner.equipment.project'
    _description = 'Main project list setup'

    name = fields.Char(string='Project name')
    project_code_crm = fields.Many2one('crm.lead')
    project_location_ids = fields.One2many('owner.equipment.project.location', 'project_location_id', store=True)
    project_category_ids = fields.One2many('owner.equipment.category', 'project_category_id', store=True)


class OwnerEquipment(models.Model):
    _name = 'owner.equipment'
    _inherit = ['mail.thread']
    _description = 'Equipment owned by client'

    name = fields.Char(string='Item name', track_visibility='onchange')
    barcode_number = fields.Char(string='Bar Code')
    project_id = fields.Many2one('owner.equipment.project', track_visibility='onchange')
    date_removed = fields.Datetime(default=lambda self: fields.datetime.now(),
                                   string='Date/Time removed',
                                   track_visibility='onchange')
    date_reinstalled = fields.Datetime(string='Date Reinstalled', track_visibility='onchange')
    removal_responsible_id = fields.Many2one('res.users',
                                             string='Removal Responsible',
                                             index=True,
                                             track_visibility='onchange',
                                             required=True,
                                             default=lambda self: self.env.uid)
    location_removed_id = fields.Many2one('owner.equipment.project.location',
                                          string='Removed from Location',
                                          track_visibility='onchange')
    sub_location_removed_id = fields.Many2one('owner.equipment.project.sublocation',
                                              string='Sub location',
                                              track_visibility='onchange')
    location_reinstalled_id = fields.Many2one('owner.equipment.project.location',
                                              string='Reinstalled Location',
                                              track_visibility='onchange')
    sub_location_reinstalled_id = fields.Many2one('owner.equipment.project.sublocation',
                                                  string='Reinstalled Sub location',
                                                  track_visibility='onchange')
    category_id = fields.Many2one('owner.equipment.category', string='Main Category', track_visibility='onchange')
    subcategory_id = fields.Many2one('owner.equipment.subcategory', string='Subcategory', track_visibility='onchange')
    stored_container_id = fields.Many2one('owner.equipment.container', track_visibility='onchange')
    description = fields.Text(string='Description', track_visibility='onchange')
    scan_history_ids = fields.One2many('owner.equipment.scan.history', 'scan_history_id', string='Scanned by')
    equipment_tracking_ids = fields.One2many('owner.equipment.tracking', 'equipment_tracking_id')
    removal_crew_ids = fields.One2many('owner.equipment.removal.crew', 'removal_crew_id')
    color = fields.Integer('Color Index')
    image = fields.Binary("Image", attachment=True)
    number_of_pieces = fields.Float(string='Number of pieces', track_visibility='onchange')
    weight = fields.Float(string='Weight in kg', track_visibility='onchange')
    total_weight = fields.Float(string='Total weight', compute='_compute_equipment_weight')
    active = fields.Boolean('Scrap', default=True, track_visibility='onchange')
    document_link = fields.Char(string='Link to documents')
    damaged = fields.Selection([('yes', 'Yes'), ('no', 'No')], default='no', string="Damaged", track_visibility='onchange')
    qaqc_item = fields.Char(string='Item number', track_visibility='onchange')
    qaqc_page = fields.Char(string='Page', track_visibility='onchange')

    @api.onchange('project_id')
    def onchange_project(self):
        self.location_removed_id = None

    @api.onchange('location_removed_id')
    def onchange_project(self):
        self.sub_location_removed_id = None

    @api.onchange('location_reinstalled_id')
    def onchange_project(self):
        self.sub_location_reinstalled_id = None

    @api.onchange('project_id')
    def onchange_project(self):
        self.category_id = None

    @api.onchange('category_id')
    def onchange_project(self):
        self.subcategory_id = None

    def _attach_image(self, file_data):
        """Attach an image to this document"""
        # Skip files that don't match the allowed extensions.
        filename = file_data.filename
        ext = filename.split('.')[-1]
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'tga', 'bmp']:
            return False
        self.image = base64.encodestring(file_data.read())
        return True

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

    @api.depends('number_of_pieces', 'weight')
    def _compute_equipment_weight(self):
        for equipment in self:
            equipment.total_weight = self.number_of_pieces * self.weight



"""        
    def create_cmis_folder_from_default_template(self, records, backend):
        self._create_in_cmis(records, backend)
        # does not work with name get for now
        # backend.create_cmis_folder_from_default_template(records,
        #                                                 backend,
        #                                                 field=self)

    def cmis_name_get(self, records, backend):
        # dict(records.name_get())
        result = []
        for record in records:
            # converts to unicode and concatenates
            # "".format does not convert from unicode it has to be done manually
            _name = ''.join((record.name, '-', record.create_date))
            result.append((record.id, _name))
        return dict(result)

    cmis_folder = cmis_fields.CmisFolder(
        backend_name=None,
        create_method=create_cmis_folder_from_default_template,
        create_name_get=cmis_name_get,
        create_parent_get=None,
        create_properties_get=None,
        allow_create=True,
        allow_delete=False,
        copy=False
    )

    @api.model
    def create(self, vals):
        res = super(OwnerEquipment, self).create(vals)
        if res:
            self._fields['cmis_folder'].create_value(res)
        return res
"""


class OwnerEquipmentContainer(models.Model):
    _name = 'owner.equipment.container'
    _inherit = ['mail.thread']
    _description = 'Storage containers (box, cartes, ect.)'

    name = fields.Char(string='Name', track_visibility='onchange')
    barcode_number = fields.Char(string='Bar Code')
    project_id = fields.Many2one('owner.equipment.project', track_visibility='onchange')
    date_removed = fields.Datetime(default=lambda self: fields.datetime.now(),
                                   string='Date/Time removed',
                                   track_visibility='onchange')
    removal_responsible_id = fields.Many2one('res.users',
                                             string='Removal Responsible',
                                             index=True,
                                             track_visibility='onchange',
                                             required=True,
                                             default=lambda self: self.env.uid)

    location_removed_id = fields.Many2one('owner.equipment.project.location',
                                          string='Removed from Location',
                                          track_visibility='onchange')

    sub_location_removed_id = fields.Many2one('owner.equipment.project.sublocation',
                                              string='Sub location',
                                              track_visibility='onchange')

    location_reinstalled_id = fields.Many2one('owner.equipment.project.location',
                                              string='Reinstalled Location',
                                              track_visibility='onchange')

    sub_location_reinstalled_id = fields.Many2one('owner.equipment.project.sublocation',
                                                  string='Reinstalled Sub location',
                                                  track_visibility='onchange')

    category_id = fields.Many2one('owner.equipment.category', string='Main Category', track_visibility='onchange')
    container_content_ids = fields.One2many('owner.equipment', 'stored_container_id', track_visibility='onchange')
    description = fields.Text(string='Description', track_visibility='onchange')

    scan_history_ids = fields.One2many('owner.equipment.scan.history', 'scan_history_id', string='Scanned by')

    equipment_tracking_ids = fields.One2many('owner.equipment.tracking', 'equipment_tracking_id')

    removal_crew_ids = fields.One2many('owner.equipment.removal.crew', 'removal_crew_id')
    color = fields.Integer('Color Index')

    image = fields.Binary("Image", attachment=True)

    number_of_pieces = fields.Float(string='Number of pieces', track_visibility='onchange')

    weight = fields.Float(string='Weight in kg', track_visibility='onchange')

    total_weight = fields.Float(string='Total weight')

    active = fields.Boolean('Scrap', default=True)

    document_link = fields.Char(string='Link to documents')

    qaqc_item = fields.Char(string='Item number', track_visibility='onchange')

    qaqc_page = fields.Char(string='Page', track_visibility='onchange')

    @api.onchange('project_id')
    def onchange_project(self):
        self.location_removed_id = None

    @api.onchange('location_removed_id')
    def onchange_project(self):
        self.sub_location_removed_id = None

    @api.onchange('location_reinstalled_id')
    def onchange_project(self):
        self.sub_location_reinstalled_id = None

    @api.onchange('project_id')
    def onchange_project(self):
        self.category_id = None

    @api.onchange('category_id')
    def onchange_project(self):
        self.subcategory_id = None

    def _attach_image(self, file_data):
        """Attach an image to this document"""
        # Skip files that don't match the allowed extensions.
        filename = file_data.filename
        ext = filename.split('.')[-1]
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'tga', 'bmp']:
            return False
        self.image = base64.encodestring(file_data.read())
        return True

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


class OwnerEquipmentProjectLocation(models.Model):
    _name = 'owner.equipment.project.location'
    _description = 'Predefined locations'

    name = fields.Char(string='Location name')
    location_code = fields.Char(string='Location code')
    project_location_id = fields.Many2one('owner.equipment.project', 'project_location_ids', store=True)
    project_sublocation_ids = fields.One2many('owner.equipment.project.sublocation', 'owner_sublocation_id')


class OwnerEquipmentProjectSublocation(models.Model):
    _name = 'owner.equipment.project.sublocation'
    _description = 'Sub location'

    name = fields.Char(string='Sub location name')
    sub_location_code = fields.Char(string='Sub location code')
    owner_sublocation_id = fields.Many2one('owner.equipment.project.location', 'project_sublocation_ids')


class OwnerEquipmentCategory(models.Model):
    _name = 'owner.equipment.category'
    _description = 'Main category'

    name = fields.Char(string='Category name')
    project_category_id = fields.Many2one('owner.equipment.project', 'project_category_ids')
    owner_subcategory_ids = fields.One2many('owner.equipment.subcategory', 'owner_subcategory_id')


class OwnerEquipmentSubcategory(models.Model):
    _name = 'owner.equipment.subcategory'
    _description = 'Subcategory'

    name = fields.Char(string='Subcategory name')
    owner_subcategory_id = fields.Many2one('owner.equipment.category', 'owner_subcategory_ids')


class OwnerEquipmentScanHistory(models.Model):
    _name = 'owner.equipment.scan.history'

    equipment_scanned_by = fields.Many2one('res.users',
                                           string='Scanned By',
                                           index=True,
                                           track_visibility='onchange',
                                           required=True,
                                           default=lambda self: self.env.uid)
    equipment_scanned_date = fields.Datetime(default=lambda self: fields.datetime.now(), string='Date/Time Scaned')
    scan_history_id = fields.Many2one('owner.equipment', 'scan_history_ids', store=True)


class OwnerEquipmentTracking(models.Model):
    _name = 'owner.equipment.tracking'

    equipment_tracking_id = fields.Many2one('owner.equipment', 'equipment_tracking_ids')
    assigned_employee = fields.Many2one('hr.employee', string='Assigned to employee')
    date_assigned_employee = fields.Datetime(default=lambda self: fields.datetime.now(), string='Date Assigned')
    assigned_location_id = fields.Many2one('owner.equipment.location')


class OwnerEquipmentLocation(models.Model):
    _name = 'owner.equipment.location'

    name = fields.Char(string='Location name')
    location_code = fields.Char(string='Location code')


class OwnerEquipmentRemovalCrew(models.Model):
    _name = 'owner.equipment.removal.crew'

    removal_crew_id = fields.Many2one('owner.equipment', 'removal_crew_ids')
    employee_crew = fields.Many2one('hr.employee', string='Crew Members')

