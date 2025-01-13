from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    name = fields.Char(translate=True)
    sub_name = fields.Char()
    is_template = fields.Boolean(
        related='project_id.is_template',
    )
    is_fse = fields.Boolean(
        string="FSE task"
    )
    is_wr = fields.Boolean(
        string="Walloon Region task"
    )
    participants = fields.One2many(
        "training.participant",
        "task_id"
    )
    participant_count = fields.Integer(
        compute='_compute_participant_count',
        store=True
    )

    @api.depends("participants", "participants.state")
    def _compute_participant_count(self):
        for task in self.filtered(lambda r: r.is_fse):
            participants = task.participants.filtered(lambda r: r.state in ['attended', 'missed'])
            task.participant_count = len(participants)
