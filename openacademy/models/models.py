# -*- coding: utf-8 -*-
from odoo import models, fields


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char('Name', required=True)
    description = fields.Html('Description')
    responsible_id = fields.Many2one('res.users', 'Responsible', ondelete='set null')
    session_ids = fields.One2many('openacademy.session', 'course_id', string='Sessions')


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char('Name')
    start_date = fields.Date('Start date')
    duration = fields.Integer('Duration')
    seats_count = fields.Integer('Seats count')
    instructor_id = fields.Many2one('res.partner', 'Instructor', ondelete='set null',
                                    domain=['|',('is_instructor','=',True),('category_id.name','like','Teacher')])
    course_id = fields.Many2one('openacademy.course', 'Course', required=True, ondelete='restrict')
    attendee_ids = fields.Many2many('res.partner', string='Attendees')



