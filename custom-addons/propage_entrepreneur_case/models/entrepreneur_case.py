# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class EntrepreneurCase(models.Model):
    _name = "entrepreneur.case"

    name = fields.Char()
    is_fse = fields.Boolean(string="Covered by FSE")
    is_decree_consultancy_agency = fields.Boolean(
        string="Covered by Wallonia Decree"
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer"
    )
    partner_email = fields.Char(
        related="partner_id.email"
    )
    partner_mobile = fields.Char(
        related="partner_id.mobile"
    )
    entrepreneur_team_id = fields.Many2one(
        "entrepreneur.team",
        string="Entrepreneur team"
    )
    team_leader_id = fields.Many2one(
        related="entrepreneur_team_id.team_leader_id"
    )
    team_leader_email = fields.Char(
        related="entrepreneur_team_id.team_leader_id.email"
    )
    team_leader_mobile = fields.Char(
        related="entrepreneur_team_id.team_leader_id.mobile"
    )
    team_member_ids = fields.Many2many(
        related="entrepreneur_team_id.team_member_ids"
    )
    crm_lead_id = fields.Many2one(
        "crm.lead",
        string="Created from lead"
    )
    project_id = fields.Many2one(
        'project.project',
        string="Project",
        copy=False
    )
    task_ids = fields.One2many(
        'project.task',
        'entrepreneur_case_id',
        string='Tasks',
        copy=False
    )
    responsible = fields.Many2one('res.users')
    convention_2c = fields.Binary(string="Convention 2C")
    covention_file_name = fields.Char()
    merchant_social_economy = fields.Boolean()
    interventio_type = fields.Selection([
        ('coaching', 'Coaching / Creation-transformation'),
        ('expertise', 'Expertise or consultancy'),
        ('post-creation', 'Post-creation follow-up')
    ],
        string="Intervention type"
    )
    intervention_start_date = fields.Date(
        string="start of intervention")
    intervention_end_date = fields.Date(
        string="End of intervention (effective or scheduled)")
    state = fields.Selection([
        ('ongoing', 'ongoing'),
        ('closed', 'Closed'),
        ('delayed', 'Delayed start'),
        ('no-news', 'No news')
    ])
    closing_type = fields.Selection([
        ('unclosed', 'Case not closed'),
        ('creation', 'Creation'),
        ('ongoing', 'End of convention or intervention'),
        ('withdrawal', 'Withdrawal')
    ])
    feasibility_study = fields.Boolean()
    legal_analysis = fields.Boolean()
    financial_analysis = fields.Boolean()
    rh = fields.Boolean(string="HR")
    financing_file_support = fields.Boolean()
    financing_received = fields.Boolean()
    amount_received = fields.Float(
        string="Amount of the received financing")
    others = fields.Boolean()
    hours_performed = fields.Float(
        string="Hours performed (past year)"
    )
    total_hours_performed = fields.Float(
        string="Hours performed (since the start)"
    )
    hours_invoiced = fields.Float(
        string="Hours invoiced (past year)"
    )
    total_hours_invoiced = fields.Float(
        string="Hours invoiced (since the start)"
    )
    created_jobs = fields.Float()
    sowescom_collaboration  = fields.Float()