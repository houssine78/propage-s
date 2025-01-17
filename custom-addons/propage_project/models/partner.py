# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    time_fse_p1 = fields.Float(compute="_compute_time_participant")
    time_fse_p2 = fields.Float(compute="_compute_time_participant")
    trainings = fields.One2many(
        'training.participant',
        'participant_id'
    )

    def _compute_time_participant(self):
        for partner in self:
            trainings = partner.trainings.filtered(
                lambda r: r.state in ['attended', 'missed']
            )
            task_time_fse_p1 = 0.0
            task_time_fse_p2 = 0.0
            for training in trainings:
                participant_count = training.task_id.participant_count
                if participant_count == 0:
                    break
                for line in training.timesheet_ids:
                    if line.timesheet_type == 'p1':
                        task_time_fse_p1 += line.unit_amount
                    elif line.timesheet_type == 'p2':
                        task_time_fse_p2 += line.unit_amount / participant_count
            partner.time_fse_p1 = task_time_fse_p1
            partner.time_fse_p2 = task_time_fse_p2
