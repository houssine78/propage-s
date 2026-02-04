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
