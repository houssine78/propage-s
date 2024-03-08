# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class Lead(models.Model):
    _inherit = "crm.lead"

    case_ids = fields.One2many(
        "entrepreneur.case",
        "crm_lead_id",
        string="Entrepreneur Case"
    )
    case_created = fields.Boolean(compute="compute_case_created")
    show_create_case = fields.Boolean(compute="compute_show_create_case", store=True)

    @api.depends("type", "stage_id", "case_ids")
    def compute_show_create_case(self):
        for lead in self:
            show = False
            if lead.type == 'opportunity' and lead.stage_id.is_won:
                if not lead.case_created:
                    show = True
            lead.show_create_case = show

    def compute_case_created(self):
        if self.case_ids:
            self.case_created = True
        else:
            self.case_created = False

    def action_create_case(self):
        case_obj = self.env['entrepreneur.case']
        vals = {
            'crm_lead_id': self.id,
            'name': self.name,
            'partner_id': self.partner_id.id
        }
        if self.convention_2c:
            vals['convention_2c'] = self.convention_2c
            vals['covention_file_name'] = self.covention_file_name

        case = case_obj.create(vals)

        return True
