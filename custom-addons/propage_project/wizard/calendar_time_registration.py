from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class TimeRegistrationWizard(models.TransientModel):
    _name = 'calendar.time.registration.wizard'
    _description = 'Create Timesheet Entries for attendees'

    calendar_event_id = fields.Many2one(
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
    lock = fields.Boolean()
            
    @api.model
    def default_get(self, fields):
        default = super().default_get(fields)
        line = self.env['calendar.time.registration.line.wizard'].sudo()
        
        if self.env.context.get('active_model') != 'calendar.event' or not self.env.context.get('active_id'):
            raise UserError(_('This can only be used on calendar event'))
        
        event = self.env['calendar.event'].browse(self.env.context['active_id'])
        default['calendar_event_id'] = event.id
        if event.timesheet_ids:
            default['project_id'] = event.timesheet_ids[0].project_id.id
            default['task_id'] = event.timesheet_ids[0].task_id.id
            default['lock'] = True

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

    def check_time(self, line):
        AnalLine = self.env['account.analytic.line'].sudo()

        if line.duration > self.calendar_event_id.duration:
            raise UserError(_("You can't register more time than the meeting duration"))

        existing_lines = AnalLine.search([
            ("calendar_event_id", "=", self.calendar_event_id.id),
            ("employee_id", "=", line.partner_id.employee_ids[0].id)
        ])
        registered_time = sum(existing_lines.mapped("unit_amount"))
        if registered_time >= self.calendar_event_id.duration:
            raise UserError(_("You can't register more time than the meeting duration"))

    def register_time(self):
        AnalLine = self.env['account.analytic.line'].sudo()
        TrainPart = self.env['training.participant'].sudo()
        # event_id = self.env.context['active_id']
        for line in self.registration_lines:
            anal_line_vals = {}
            train_part_vals = {}
            
            if line.is_employee:
                self.check_time(line)
                if line.is_fse:
                    if not line.timesheet_type:
                        raise UserError(_('You need to give a timesheet_type for the employee'))
                    anal_line_vals['timesheet_type'] = line.timesheet_type
                anal_line_vals['date'] = line.date
                anal_line_vals['employee_id'] = line.partner_id.employee_ids[0].id
                anal_line_vals['name'] = line.name
                anal_line_vals['task_id'] = line.time_registration_id.task_id.id
                anal_line_vals['unit_amount'] = line.duration
                anal_line_vals['customer_id'] = line.customer_id.id
                anal_line_vals['calendar_event_id'] = self.calendar_event_id.id

                AnalLine.create(anal_line_vals)
            else:
                train_part_vals['participant_id'] = line.partner_id.id
                train_part_vals['task_id'] = line.time_registration_id.task_id.id
                train_part_vals['training_date'] = line.date
                train_part_vals['state'] = 'attended'
                train_part_vals['calendar_event_id'] = self.calendar_event_id.id
                TrainPart.create(train_part_vals)


class TimeRegistrationLineWizard(models.TransientModel):
    _name = 'calendar.time.registration.line.wizard'

    name = fields.Char(string="Description")
    partner_id = fields.Many2one("res.partner") 
    duration = fields.Float()
    date = fields.Date()
    time_registration_id = fields.Many2one("calendar.time.registration.wizard")
    is_employee = fields.Boolean(related="partner_id.is_employee")
    is_fse = fields.Boolean(related="time_registration_id.task_id.is_fse")
    timesheet_type = fields.Selection([
        ('p1', 'P1'),
        ('p2', 'P2'),
        ('p3', 'P3')],
        string="Type",
    )
    customer_id = fields.Many2one('res.partner')
