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