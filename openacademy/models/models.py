# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
from datetime import timedelta

_logger = logging.getLogger(__name__)


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    responsible_id = fields.Many2one('res.users', 'Responsible', ondelete='set null')
    session_ids = fields.One2many('openacademy.session', 'course_id', string='Sessions')

    _sql_constraints = [
        ('course_desc_not_title','CHECK(description != name)','Course name and description must be different!'),
        ('course_name_unique','UNIQUE(name)','Course name must be unique!')
    ]

    def copy(self):
        for rec in self:
            return super(Course, rec).copy(default={'name': f'Copy of {rec.name}'})


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char('Name')
    start_date = fields.Date('Start date', default=lambda self: fields.Date.context_today(self))
    end_date = fields.Date('End date', compute='_compute_end_date')
    duration = fields.Integer('Duration')
    seats_total = fields.Integer('Seats total')
    seats_taken = fields.Integer('Taken seats', compute='_compute_seats_taken')
    instructor_id = fields.Many2one('res.partner', 'Instructor', ondelete='set null',
                                    domain=['|',('is_instructor','=',True),('category_id.name','like','Teacher')])
    course_id = fields.Many2one('openacademy.course', 'Course', required=True, ondelete='restrict')
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    active = fields.Boolean('Active', default=True)

    @api.depends('seats_total','attendee_ids')
    def _compute_seats_taken(self):
        for rec in self:
            if rec.attendee_ids and rec.seats_total:
                rec.seats_taken = round(len(rec.attendee_ids) * 100 / rec.seats_total)
            else:
                rec.seats_taken = 0

    @api.onchange('seats_total','attendee_ids')
    def _onchange_seats_taken(self):
        def warn_response(message):
            return {
                'warning': {
                'title': 'Something bad happened',
                'message': message,
                }
            }
        if self.seats_total < 0:
            return warn_response('Seats total must be positive!')
        elif self.seats_total < len(self.attendee_ids):
            return warn_response(f'Too many participants (max {self.seats_total})!')

    @api.constrains('instructor_id')
    def _check_instructor_is_attendee(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id not in rec.attendee_ids:
                raise ValidationError('Instructor must be in attendee list!')

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.duration:
                rec.end_date = rec.start_date + timedelta(rec.duration)
            else:
                rec.end_date = False



