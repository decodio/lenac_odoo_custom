# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2020 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools, _
from odoo.addons.cmis_field import fields as cmis_fields


class OwnerEquipment(models.Model):
    _inherit = 'owner.equipment'

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
