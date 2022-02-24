# -*- coding: utf-8 -*-
# Copyright © 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, _


class RestApiModel(models.Model):
    _inherit = "rest.api.model"

    def create_owner_equipment(self, name, barcode_number, project_id, removal_responsible_id,
                               location_removed_id, category_id, subcategory_id=False, image=False,
                               description=False, number_of_pieces=False, weight=False, document_link=False,
                               active=False, damaged=False):
        """ Create an new equipment with all the above filed required """
        try:
            vals = {
                'name': name,
                'barcode_number': barcode_number,
                'project_id': int(project_id),
                'removal_responsible_id': int(removal_responsible_id),
                'location_removed_id': int(location_removed_id),
                'category_id': int(category_id),
                'subcategory_id': int(subcategory_id),
                'description': description,
                'number_of_pieces': number_of_pieces,
                'weight': weight,
                'document_link': document_link,
                'active': active,
                'damaged': damaged
            }
            owner_equipment_model = self.env['owner.equipment']
            res = owner_equipment_model.create(vals)
            if res:
                # Crate and attach an image
                res._attach_image(image)
                return{'result': {'id': res.id},
                       'success': True,
                       'message': ''}
            else:
                return {'result': '',
                        'success': False,
                        'message': ''}
        except Exception as e:
            return {'result': '',
                    'success': False,
                    'message': str(e)}

    def update_owner_equipment(self, res_id, **kwargs):
        """ Update existing equipment"""
        optional_fields = ['name', 'description', 'date_reinstalled', 'weight', 'number_of_pieces', 'document_link']

        int_fields = ['project_id',
                      'removal_responsible_id',
                      'location_removed_id',
                      'location_reinstalled_id'
                      'category_id',
                      'subcategory_id']

        try:
            # Extract optional values from incoming arguments
            vals = {}
            for key in optional_fields:
                if key not in kwargs:
                    continue
                value = kwargs.get(key)
                # Try to parse the value if possible
                if key in int_fields:
                    vals[key] = int(value)
                else:
                    vals[key] = value

            owner_equipment_model = self.env['owner.equipment']
            eq_id = owner_equipment_model.search(
                [('id', '=', int(res_id))], limit=1)
            res = False
            if eq_id and vals:
                res = eq_id.write(vals)
            if res:
                return {'result': res,
                        'success': True,
                        'message': ''}
            else:
                return {'result': res,
                        'success': False,
                        'message': ''}

        except Exception as e:
            return {'result': '',
                    'success': False,
                    'message': str(e)}

    def create_owner_scan_history(self, equipment_scanned_by, scan_history_id):
        """ Create an new equipment with all the above filed required """
        try:
            vals = {
                'equipment_scanned_by': int(equipment_scanned_by),
                'scan_history_id': int(scan_history_id),
            }
            owner_equipment_scan_history_model = self.env['owner.equipment.scan.history']
            res = owner_equipment_scan_history_model.create(vals)
            if res:
                return{'result': {'id': res.id},
                       'success': True,
                       'message': ''}
            else:
                return {'result': '',
                        'success': False,
                        'message': ''}
        except Exception as e:
            return {'result': '',
                    'success': False,
                    'message': str(e)}

    def create_owner_equipment_tracking(self, equipment_tracking_id, assigned_employee, assigned_location_id):
        """ Create an new equipment with all the above filed required """
        try:
            vals = {
                'equipment_tracking_id': int(equipment_tracking_id),
                'assigned_employee': int(assigned_employee),
                'assigned_location_id': int(assigned_location_id)
            }
            owner_equipment_tracking_model = self.env['owner.equipment.tracking']
            res = owner_equipment_tracking_model.create(vals)
            if res:
                return{'result': {'id': res.id},
                       'success': True,
                       'message': ''}
            else:
                return {'result': '',
                        'success': False,
                        'message': ''}
        except Exception as e:
            return {'result': '',
                    'success': False,
                    'message': str(e)}

    def create_owner_equipment_container(self, name, barcode_number, project_id, removal_responsible_id,
                                         location_removed_id, category_id, image=False, description=False,
                                         number_of_pieces=False, weight=False, document_link=False, active=False):
        """ Create an new equipment container with all the above filed required """
        try:
            vals = {
                'name': name,
                'barcode_number': barcode_number,
                'project_id': int(project_id),
                'removal_responsible_id': int(removal_responsible_id),
                'location_removed_id': int(location_removed_id),
                'category_id': int(category_id),
                'description': description,
                'number_of_pieces': number_of_pieces,
                'weight': weight,
                'document_link': document_link,
                'active': active
            }
            owner_equipment_container_model = self.env['owner.equipment.container']
            res = owner_equipment_container_model.create(vals)
            if res:
                # Crate and attach an image
                res._attach_image(image)
                return{'result': {'id': res.id},
                       'success': True,
                       'message': ''}
            else:
                return {'result': '',
                        'success': False,
                        'message': ''}
        except Exception as e:
            return {'result': '',
                    'success': False,
                    'message': str(e)}

    def update_owner_equipment_container(self, res_id, **kwargs):
        """ Update existing equipment container"""
        optional_fields = ['name', 'description', 'date_reinstalled', 'weight', 'number_of_pieces', 'document_link']

        int_fields = ['project_id',
                      'removal_responsible_id',
                      'location_removed_id',
                      'location_reinstalled_id'
                      'category_id'
                      ]

        try:
            # Extract optional values from incoming arguments
            vals = {}
            for key in optional_fields:
                if key not in kwargs:
                    continue
                value = kwargs.get(key)
                # Try to parse the value if possible
                if key in int_fields:
                    vals[key] = int(value)
                else:
                    vals[key] = value

            owner_equipment_container_model = self.env['owner.equipment.container']
            eq_id = owner_equipment_container_model.search(
                [('id', '=', int(res_id))], limit=1)
            res = False
            if eq_id and vals:
                res = eq_id.write(vals)
            if res:
                return {'result': res,
                        'success': True,
                        'message': ''}
            else:
                return {'result': res,
                        'success': False,
                        'message': ''}

        except Exception as e:
            return {'result': '',
                    'success': False,
                    'message': str(e)}
