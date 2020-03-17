# -*- coding: utf-8 -*-
# Odoo, Open Source Management Solution
# Copyright (C) 2018 Vedran Terihaj
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models, fields, _


class HrLunch(models.Model):
    _name = 'hr.lunch'

    name = fields.Char()
    lunch_break_id = fields.Many2one('hr.job.long')


class HrWorkTools(models.Model):
    _name = 'hr.work.tools'

    name = fields.Char()
    work_tools_id = fields.Many2one('hr.job.long')


class HrWorkMaterials(models.Model):
    _name = 'hr.work.materials'

    name = fields.Char()
    work_materials_id = fields.Many2one('hr.job.long')


class HrWorkPlace(models.Model):
    _name = 'hr.work.place'

    name = fields.Char()
    work_place_description = fields.Text()
    work_place_id = fields.Many2one('hr.job.long')


class HrProtectionGear(models.Model):
    _name = 'hr.protection.gear'

    name = fields.Char()
    protection_body_part = fields.Many2one('hr.body.part')
    protection_gear1_id = fields.Many2one('hr.job.long')
    protection_gear2_id = fields.Many2one('hr.job.long')
    protection_gear3_id = fields.Many2one('hr.job.long')
    protection_gear4_id = fields.Many2one('hr.job.long')
    protection_gear5_id = fields.Many2one('hr.job.long')
    protection_gear6_id = fields.Many2one('hr.job.long')
    protection_gear7_id = fields.Many2one('hr.job.long')
    protection_gear8_id = fields.Many2one('hr.job.long')


class HrBodyPart(models.Model):
    _name = 'hr.body.part'

    name = fields.Char()


class HrRisk(models.Model):
    _name = 'hr.risk'

    name = fields.Char()
    danger_ids = fields.Many2many('hr.dangers', 'danger_id')
    consequence_ids = fields.Many2many('hr.consequence', 'consequence_id')
    risk_measures = fields.Html()

    field_1 = fields.Selection([('A', 'A'),
                                ('B', 'B'),
                                ('C', 'C'),
                                ('D', 'D'),
                                ('E', 'E')])
    field_2 = fields.Selection([(1, '1'),
                                (2, '2'),
                                (3, '3'),
                                (4, '4'),
                                (5, '5')])

    field_3 = fields.Char(track_visibility='onchange')

    @api.onchange('field_1', 'field_2')
    def onchange_fields12(self):
        if not self.field_1 or not self.field_2:
            return False

        #  key = vriednost polja field_1
        #  val = lista vrijednosti polja field_2
        vals_mapper = {
            'A': [1, 1, 1, 1, 2],
            'B': [1, 1, 1, 2, 2],
            'C': [1, 1, 2, 2, 3],
            'D': [1, 2, 2, 3, 3],
            'E': [2, 2, 3, 3, 3]
        }

        vals_list = vals_mapper.get(self.field_1)
        #if self.field_2 not in vals_list:
        #    raise Exception('Wrong value received')
        # field_2 mora imati integer vrijednosti 1 -5 !
        self.field_3 = vals_list[self.field_2 - 1]

    field_4 = fields.Selection([('A', 'A'),
                                ('B', 'B'),
                                ('C', 'C'),
                                ('D', 'D'),
                                ('E', 'E')])
    field_5 = fields.Selection([(1, '1'),
                                (2, '2'),
                                (3, '3'),
                                (4, '4'),
                                (5, '5')])

    field_6 = fields.Char(track_visibility='onchange')

    @api.onchange('field_4', 'field_5')
    def onchange_fields56(self):
        if not self.field_4 or not self.field_5:
            return False

        #  key = vriednost polja field_1
        #  val = lista vrijednosti polja field_2
        vals_mapper = {
            'A': [1, 1, 1, 1, 2],
            'B': [1, 1, 1, 2, 2],
            'C': [1, 1, 2, 2, 3],
            'D': [1, 2, 2, 3, 3],
            'E': [2, 2, 3, 3, 3]
        }

        vals_list = vals_mapper.get(self.field_4)
        # if self.field_2 not in vals_list:
        #    raise Exception('Wrong value received')
        # field_2 mora imati integer vrijednosti 1 -5 !
        self.field_6 = vals_list[self.field_5 - 1]


class HrDangers(models.Model):
    _name = 'hr.dangers'

    name = fields.Char()


class HrConsequence(models.Model):
    _name = 'hr.consequence'

    name = fields.Char()


class HRMandatoryQualification (models.Model):
    _name = 'hr.mandatory.qualification'

    name = fields.Char()
    mandatory_qualification_id = fields.Many2one('hr.job.long')

