from odoo import fields, models


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
    training_time = fields.Float("Training Hours")

    # def compute_time_p1(self, training_time):
    #     attendees_count = self.env['training.participant'].search([
    #         ('task_id', '=', self.id),
    #         ('state', '=', 'attended')
    #     ])
    #     time_p1 = training_time * attendees_count
    #     line_p1 = self.env['account.analytic.line'].search([
    #         ('task_id', '=', self.id),
    #         ('timesheeet_type', '=', 'p1')
    #     ], limit=1)
    #     if time_p1 > 0 and line_p1:
    #         line_p1.write({'':time_p1})
    #         print("ohohoh")
    #     return True
    #
    # def write(self, vals):
    #     res = super(ProjectTask, self).write(vals)
    #     if 'training_time' in vals:
    #         training_time = vals.get('training_time')
    #         self.compute_time_p1(training_time)
    #
    #     return res
