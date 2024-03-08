# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    is_won = fields.Boolean(related='stage_id.is_won')
    convention_2c = fields.Binary(string="Convention 2C")
    covention_file_name = fields.Char()
