# Copyright 2025 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date
from odoo import api, fields, models


class FSETimeLog(models.Model):
    _name = 'fse.time.log'
    _description = 'FSE Time Log'

    _sql_constraints = [
        (
            'partner_year_unique',
            'UNIQUE(partner_id, year)',
            'A FSE time log entry already exists for this partner and year.',
        ),
    ]

    partner_id = fields.Many2one('res.partner', required=True)
    year = fields.Char(required=True)
    time_fse_p1 = fields.Float(
        compute="_compute_time_participant",
        store=True
    )
    time_fse_p2 = fields.Float(
        compute="_compute_time_participant",
        store=True
    )

    @api.depends(
        'year',
        'partner_id.trainings',
        'partner_id.trainings.state',
        'partner_id.trainings.training_date',
        'partner_id.trainings.task_id',
        'partner_id.trainings.task_id.participant_count',
        'partner_id.trainings.timesheet_ids',
        'partner_id.trainings.timesheet_ids.timesheet_type',
        'partner_id.trainings.timesheet_ids.unit_amount',
    )
    def _compute_time_participant(self):
        for fse_time_log in self:
            start_date = date(int(fse_time_log.year), 1, 1)
            end_date = date(int(fse_time_log.year), 12, 31)
            trainings = fse_time_log.partner_id.trainings.filtered(
                lambda r: r.state in ['attended', 'missed'] and
                          r.training_date >= start_date and
                          r.training_date <= end_date
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
            fse_time_log.time_fse_p1 = task_time_fse_p1
            fse_time_log.time_fse_p2 = task_time_fse_p2
