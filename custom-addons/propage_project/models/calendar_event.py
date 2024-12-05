from odoo import api,fields, models

class Meeting(models.Model):
    _inherit = 'calendar.event'

    time_registered = fields.Boolean()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_employee = fields.Boolean(
        compute="_compute_is_employee",
        store=True
    )

    @api.depends("employee_ids")
    def _compute_is_employee(self):
        for partner in self:
            if partner.employees_count > 0:
                partner.is_employee = True