# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EntrepreneurCase(models.Model):
    _name = "entrepreneur.case"

    name = fields.Char()
    entrepreneur_team_id = fields.Many2one(
        "entrepreneur.team",
        string="Entrepreneur team"
    )
    team_leader_id = fields.Many2one(
        related="entrepreneur_team_id.team_leader_id"
    )
    team_member_ids = fields.Many2many(
        related="entrepreneur_team_id.team_member_ids"
    )
    crm_lead_id = fields.Many2one(
        "crm.lead",
        string="Created from lead"
    )
    is_fse = fields.Boolean(
        string="Covered by FSE"
    )
    is_decree_consultancy_agency = fields.Boolean(
        string="Covered by Wallonia Decree"
    )
