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
    time_fse_p1 = fields.Float(compute="_compute_time_participant")
    time_fse_p2 = fields.Float(compute="_compute_time_participant")

    @api.depends("employee_ids")
    def _compute_is_employee(self):
        for partner in self:
            if partner.employees_count > 0:
                partner.is_employee = True

    def _compute_time_participant(self):
        for partner in self:
            time_fse_p1 = 0
            time_fse_p2 = 0
    
            for time_log in self.fse_time_log_ids:
                time_fse_p1 += time_log.time_fse_p1
                time_fse_p2 += time_log.time_fse_p2
    
            partner.time_fse_p1 = time_fse_p1
            partner.time_fse_p2 = time_fse_p2

    @api.model_create_multi
    def create(self, vals_list):
        partners = super(Partner, self).create(vals_list)
        year = fields.Date.today().year
        
        for partner in partners:
            if partner.is_entrepreneur:
                fse_vals_list = [
                    {'partner_id': partner.id, 'year': str(year)},
                    {'partner_id': partner.id, 'year': str(year - 1)},
                    {'partner_id': partner.id, 'year': str(year - 2)},
                ]
                self.env['fse.time.log'].create(fse_vals_list)
        return partners

    def write(self, vals):
        res = super(Partner, self).write(vals)

        year = fields.Date.today().year

        for partner in self:
            if partner.is_entrepreneur and len(partner.fse_time_log_ids) == 0:
                fse_vals_list = [
                    {'partner_id': partner.id, 'year': str(year)},
                    {'partner_id': partner.id, 'year': str(year - 1)},
                    {'partner_id': partner.id, 'year': str(year - 2)},
                ]
                self.env['fse.time.log'].create(fse_vals_list)
        return res
