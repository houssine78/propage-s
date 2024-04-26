from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    entrepreneur_case_id = fields.Many2one(
        'entrepreneur.case',
        string="Entrepeneur case"
    )
