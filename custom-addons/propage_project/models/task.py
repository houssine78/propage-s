from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    name = fields.Char(translate=True)
    sub_name = fields.Char()
    is_template = fields.Boolean(
        related='project_id.is_template',
    )