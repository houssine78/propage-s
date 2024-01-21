# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EntrepreneurProjectTeam(models.Model):
    _name = "entrepreneur.team"

    name = fields.Char()
    team_leader_id = fields.Many2one(
        "res.partner"
    )
    team_member_ids = fields.Many2many(
        "res.partner",
        string="Project members"
    )
    entrepreneur_case_ids = fields.One2many(
        "entrepreneur.case",
        "entrepreneur_team_id"
    )
