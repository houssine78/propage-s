# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    case_ids = fields.One2many(
        "entrepreneur.case",
        "crm_lead_id",
        string="Entrepreneur Case"
    )

    def action_create_case(self):
        case_obj = self.env['entrepreneur.case']
        vals = {
            'crm_lead_id': self.id,
            'name': self.name,
            'partner_id': self.partner_id.id
        }
        case = case_obj.create(vals)

        return True
