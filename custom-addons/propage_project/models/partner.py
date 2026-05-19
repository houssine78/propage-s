# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    fse_time_log_ids = fields.One2many('fse.time.log', 'partner_id')
    trainings = fields.One2many(
        'training.participant',
        'participant_id'
    )
    is_employee = fields.Boolean(
        compute="_compute_is_employee",
        store=True
    )
    time_fse_p1 = fields.Float(
        compute="_compute_time_participant",
        store=True
    )
    time_fse_p2 = fields.Float(
        compute="_compute_time_participant",
        store=True
    )
    timesheet_matrix_ids = fields.One2many(
        'partner.timesheet.matrix',
        'partner_id',
        compute='_compute_timesheet_matrix',
        string="Matrice des temps",
        store=True
    )
    timesheet_ids = fields.One2many(
        'account.analytic.line',
        'customer_id'
    )

    @api.depends('timesheet_ids', 'timesheet_ids.customer_id', 'timesheet_ids.task_id.is_wr')    
    def _compute_timesheet_matrix(self):
        for partner in self:
            matrix_data = {}

            for line in self.timesheet_ids.filtered(
                    lambda t: t.task_id and t.task_id.is_wr and t.customer_id.id == partner.id
                ):
                year = str(line.date.year)
                task_id = line.task_id.id
                key = (year, task_id)
                
                if key not in matrix_data:
                    matrix_data[key] = 0.0
                matrix_data[key] += line.unit_amount
            
            matrix_data = dict(sorted(matrix_data.items()))
            
            commands = [(5, 0, 0)]
            for (year, task_id), amount in matrix_data.items():
                commands.append((0, 0, {
                    'year': year,
                    'task_id': task_id,
                    'amount': amount,
                }))
            partner.timesheet_matrix_ids = commands

    @api.depends("employee_ids")
    def _compute_is_employee(self):
        for partner in self:
            if partner.employees_count > 0:
                partner.is_employee = True

    @api.depends(
        "fse_time_log_ids",
        "fse_time_log_ids.partner_id",
        "fse_time_log_ids.time_fse_p1",
        "fse_time_log_ids.time_fse_p2"
    )
    def _compute_time_participant(self):
        for partner in self:
            time_fse_p1 = 0
            time_fse_p2 = 0

            for time_log in partner.fse_time_log_ids:
                time_fse_p1 += time_log.time_fse_p1
                time_fse_p2 += time_log.time_fse_p2

            partner.time_fse_p1 = time_fse_p1
            partner.time_fse_p2 = time_fse_p2

    def action_recompute_time_participant(self):
        self._compute_time_participant()

    def action_create_fse_time_log_years(self):
        year = fields.Date.today().year
        if not self.fse_time_log_ids:
            self.init_time_log()
            return True
        if str(year) not in self.fse_time_log_ids.mapped('year'):
            vals = {
                'partner_id': self.id,
                'year': str(year)
            }
            self.env['fse.time.log'].create(vals)
        return True

    def init_time_log(self):
        year = fields.Date.today().year
        existing_years = set(self.fse_time_log_ids.mapped('year'))
        fse_vals_list = [
            {'partner_id': self.id, 'year': str(y)}
            for y in [year, year - 1, year - 2]
            if str(y) not in existing_years
        ]
        if fse_vals_list:
            self.env['fse.time.log'].create(fse_vals_list)

    @api.model_create_multi
    def create(self, vals_list):
        partners = super(Partner, self).create(vals_list)
        
        for partner in partners:
            if partner.is_entrepreneur:
                partner.init_time_log()
        return partners

    def write(self, vals):
        res = super(Partner, self).write(vals)

        for partner in self:
            if partner.is_entrepreneur and len(partner.fse_time_log_ids) == 0:
                partner.init_time_log()
        return res
