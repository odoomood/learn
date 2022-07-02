# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean('Instructor')
    session_ids = fields.Many2many('openacademy.session', string='Sessions')
