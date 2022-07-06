# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AttendeesWizard(models.TransientModel):
    _name = 'openacademy.attendees.wizard'

    # def _default_attendees(self):
    #     sessions = self.env['openacademy.session'].browse(self._context.get('active_ids'))
    #     if sessions:
    #         return sessions.attendee_ids
    #     else:
    #         return False

    session_ids = fields.Many2many('openacademy.session', string='Session(s)',
                                 default=lambda self: self._context.get('active_ids'))
    attendee_ids = fields.Many2many(
        'res.partner', string='Attendees',
        default=lambda self: self.env['openacademy.session'].browse(self._context.get('active_ids')).attendee_ids
    )

    def save_attendees(self):
        sessions = self.env['openacademy.session'].browse(self.session_ids.ids)
        for session in sessions:
            session.attendee_ids = self.attendee_ids
