# -*- coding: utf-8 -*-
# Copyright © 2017 Decodio Applications d.o.o.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, _


class RestApiModel(models.Model):
    _inherit = "rest.api.model"

    def create_maintenance_equipment(self, name, sort_of_equipment, category_id,
                                     pc_number, equipment_assign_to,
                                     employee_id, date_assigned, new_location,
                                     old_equipment_assign_to, old_employee_id,
                                     assign_date, date_purchased,
                                     partner_ref, item_model, serial_no, barcode_number, location=None):
        """ Create an new equipment with all the above filed required """
        try:
            vals = {
                'name': name,
                'sort_of_equipment': sort_of_equipment,

                #'sm_equipment_assign_to': 'other'
                # sort_of_equipment selection: ict, sm_production, production

                'category_id': int(category_id), # category id goes here
                'pc_number': pc_number,

                'equipment_assign_to': equipment_assign_to,
                # equipment_assign_to selection: employee, department, other

                'employee_id': int(employee_id),
                'date_assigned': date_assigned,
                'new_location': new_location,

                'old_equipment_assign_to': old_equipment_assign_to,
                # old_equipment_assign_to selection: employee, department, other

                'old_employee_id': int(old_employee_id),
                'assign_date': assign_date,
                'location': location,
                'date_purchased': date_purchased,
                'partner_ref': partner_ref,
                # model is an reserved function field so use
                # another field name instead
                'model': item_model,
                # Reći Ikici da umjesto model šalje item_model
                'serial_no': serial_no,
                'barcode_number': barcode_number
            }

            maintenance_equipment_model = self.env['maintenance.equipment']
            res = maintenance_equipment_model.create(vals)
            if res:
                return {'result': {'equipment_id': res.id},
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

    def update_maintenance_equipment(self, res_id, **kwargs):
        """ Update existing maintenance equipment"""
        optional_fields = ['name', 'category_id', 'pc_number',
                           'equipment_assign_to', 'employee_id',
                           'date_assigned', 'new_location',
                           'old_equipment_assign_to', 'old_employee_id',
                           'assign_date', 'location', 'barcode_number',
                           'sort_of_equipment']

        int_fields = ['category_id',
                      'equipment_assign_to',
                      'employee_id',
                      'old_equipment_assign_to',
                      'old_employee_id']
        #todo
        """ Ovaj update također mora mjenjati polje sm_equipment_ids
            Polja koja ažurira su iz modela maintenance.employee.tracking
            sm_equipment_assign_to --> selection polje  employee , other
            sm_employee_id
            smo_employee_id
            tool_shop_ids
        """

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

            maintenance_equipment_model = self.env['maintenance.equipment']
            eq_id = maintenance_equipment_model.search(
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

    def create_maintenance_equipment_tracking(self, sm_equipment_id,
                                              sm_employee_id, tool_shop_id, bar_code):
        """ Create a new equipment tracking record
         with all the above filed required """
        try:
            vals = {
                'sm_equipment_id': int(sm_equipment_id),
                'sm_employee_id': int(sm_employee_id),
                'tool_shop_id': int(tool_shop_id),
                'bar_code': bar_code,
                'sm_equipment_assign_to': 'other'
            }

            maintenance_equipment_tracking_model = self.env[
                'maintenance.equipment.tracking']
            res = maintenance_equipment_tracking_model.create(vals)
            if res:
                return {'result': {'maintenance_equipment_tracking_id': res.id},
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

    def update_maintenance_equipment_tracking(self, res_id, **kwargs):
        """ Update existing maintenance equipment tracking """
        optional_fields = ['sm_equipment_id',
                           'sm_employee_id',
                           'tool_shop_id',
                           'sm_equipment_assign_to',
                           'smo_employee_id',
                           'bar_code']

        int_fields = ['sm_equipment_id',
                      'sm_employee_id',
                      'tool_shop_id',
                      'smo_employee_id']
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

            maintenance_equipment_tracking_model = self.env[
                'maintenance.equipment.tracking']
            eqt_id = maintenance_equipment_tracking_model.search(
                [('id', '=', int(res_id))], limit=1)
            res = False
            if eqt_id and vals:
                res = eqt_id.write(vals)
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
