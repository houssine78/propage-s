from odoo import api, fields, models


class Meeting(models.Model):
    _inherit = 'calendar.event'

    name = fields.Char(required=False)
    timesheet_ids = fields.One2many(
        "account.analytic.line",
        "calendar_event_id"
    )
    participant_ids = fields.One2many(
        "training.participant",
        "calendar_event_id"
    )
    meeting_type_id = fields.Many2one(
        "meeting.type",
        required=True
    )
    calendar_warning = fields.Boolean(
        compute="_compute_calendar_warning"
    )

    def _compute_calendar_warning(self):
        for calendar in self:
            warning = False
            if calendar.timesheet_ids:
                warning = calendar.timesheet_ids.mapped("calendar_warning")[0]
            calendar.calendar_warning = warning

    @api.depends('name', 'meeting_type_id', 'timesheet_ids')
    def _compute_display_name(self):
        for record in self:
            if record.timesheet_ids:
                timesheet = record.timesheet_ids[0]
                project = timesheet.project_id.name
                task = timesheet.task_id.name
                meeting_type = record.meeting_type_id.name or ""
                record.display_name = f"{record.name}\n{meeting_type}\n{project}\n{task}" 
            else:
                super(Meeting, record)._compute_display_name()
