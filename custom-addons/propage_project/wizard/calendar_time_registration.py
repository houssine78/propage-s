from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from test.test_pdb import do_something

class TimeRegistrationWizard(models.TransientModel):
    _name = 'calendar.time.registration.wizard'
    _description = 'Create Timesheet Entries for attendees'

    event_id = fields.Many2one(
        'calendar.event',
        required=True
    )
    project_id = fields.Many2one(
        'project.project',
        required=True)
    task_id = fields.Many2one(
        'project.task',
        required=True
    )
    registration_lines = fields.One2many(
        'calendar.time.registration.line.wizard',
        'time_registration_id'
    )

    @api.model
    def default_get(self, fields):
        default = super().default_get(fields)
        line = self.env['calendar.time.registration.line.wizard'].sudo()
        
        if self.env.context.get('active_model') != 'calendar.event' or not self.env.context.get('active_id'):
            raise UserError(_('This can only be used on calendar event'))
        
        event = self.env['calendar.event'].browse(self.env.context['active_id'])
        default['event_id'] = event.id

        line_vals = []
        for partner in event.partner_ids:
            vals = {}
            vals['partner_id'] = partner.id
            vals['duration'] = event.duration
            vals['date'] = event.start
            vals['time_registration_id'] = self.id
            line_vals.append(vals)
        lines = line.create(line_vals)
        default['registration_lines'] = [(6, 0, lines.ids)]
        return default

    def register_time(self):
        anal_line = self.env['account.analytic.line'].sudo()
        train_part = self.env['training.participant'].sudo()
        
        for line in self.registration_lines:
            anal_line_vals = {}
            train_part_vals = {}
            if line.is_employee:
                if line.is_fse:
                    anal_line_vals['timesheeet_type'] = line.timesheeet_type
                anal_line_vals['date'] = line.date
                anal_line_vals['employee_id'] = line.partner_id.employee_ids[0].id
                anal_line_vals['name'] = line.name
                anal_line_vals['task_id'] = line.time_registration_id.task_id.id
                anal_line_vals['unit_amount'] = line.duration

                anal_line.create(anal_line_vals)
            else:
                train_part_vals['participant'] = line.partner_id.id
                train_part_vals['task_id'] = line.time_registration_id.task_id.id
                train_part_vals['training_date'] = line.date
                train_part_vals['state'] = 'attended'
                train_part.create(train_part_vals)
                line.time_registration_id.task_id.training_time = line.duration 
        self.event_id.time_registered = True

class TimeRegistrationLineWizard(models.TransientModel):
    _name = 'calendar.time.registration.line.wizard'

    name = fields.Char(string="Description")
    partner_id = fields.Many2one("res.partner") 
    duration = fields.Float()
    date = fields.Date()
    time_registration_id = fields.Many2one("calendar.time.registration.wizard")
    is_employee = fields.Boolean(related="partner_id.is_employee")
    is_fse = fields.Boolean(related="time_registration_id.task_id.is_fse")
    timesheeet_type = fields.Selection([
        ('p1', 'P1'),
        ('p2', 'P2'),
        ('p3', 'P3'),
        ],
        string="Type",
    )

