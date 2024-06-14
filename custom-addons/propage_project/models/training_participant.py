from odoo import fields, models


class TrainingParticpant(models.Model):
    _name = "training.participant"

    participant = fields.Many2one(
        "res.partner",
        required = True,
        domain = [('is_entrepreneur', '=', True)]
    )
    state = fields.Selection([
        ('draft', 'draft'),
        ('attended', 'Attended'),
        ('declined', 'Declined'),
        ('missed', 'Missed')],
        default='draft'
    )
    task_id = fields.Many2one(
        "project.task",
        string="Task",
        required = True
    )

    def action_attended(self):
        self.write({'state': 'attended'})

    def action_missed(self):
        self.write({'state': 'missed'})

    def action_declined(self):
        self.write({'state': 'declined'})
    