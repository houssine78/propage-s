from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    timesheet_type = fields.Selection([
        ('p1', 'P1'),
        ('p2', 'P2'),
        ('p3', 'P3'),
        ],
        string="Type",
    )
    is_fse = fields.Boolean(related="task_id.is_fse")
    customer_id = fields.Many2one("res.partner")
    calendar_event_id = fields.Many2one("calendar.event")
    calendar_warning = fields.Boolean(
        compute="_compute_calendar_warning",
        help="Technical computed field to warn when not enough time is "
             "registered for the calendar event timesheet"
    )

    def _compute_calendar_warning(self):
        AnalLine = self.env['account.analytic.line'].sudo()

        for line in self:
            event_id = line.calendar_event_id
            calendar_warning = False
            if event_id:
                duration = event_id.duration
                lines = line.task_id.timesheet_ids.filtered(
                            lambda l: l.calendar_event_id.id == event_id.id and
                                      l.employee_id.id == line.employee_id.id
                )
                if sum(lines.mapped('unit_amount')) < duration:
                    calendar_warning = True
                line.calendar_warning = calendar_warning
