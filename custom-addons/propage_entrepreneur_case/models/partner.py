# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_entrepreneur = fields.Boolean()
    fse_id = fields.Integer()
    professional_status = fields.Selection([
        ('employee', 'Employee'),
        ('independent', 'Independent worker'),
        ('job_seeker', 'Job seeker'),
        ('cpas', 'CPAS (incl. art.60&61)'),
        ('inactive_alt_education', 'Inactive alternative education'),
        ('inactive_education', 'Inactive education'),
        ('inactive_other', 'Inactive other')
        ],
        string="Professional status"
    )
    inactive_period = fields.Selection([
        ('employee', 'Employee'),
        ('independent', 'Independent worker'),
        ('unemployed', 'Unemployed')
        ],
        string="Inactive period"
    )
    education_level = fields.Selection([
        ('first_cycle_second', 'Max. first cycle of secondary (CITE 0 to 2)'),
        ('post_second_school', 'Max. post secondary school (CITE 3 to 4)'),
        ('higher_education', 'Higher education (CITE 5 to 8)')
        ],
        string="Education level"
    )
    action_start_date = fields.Date(
        string="Action start date"
    )
    action_end_date = fields.Date(
        string="Action end date"
    )
    cumulive_total_hours = fields.Float(
        string="Cumulative total hours"
    )
    end_type = fields.Selection([
        ('employee', 'Employee'),
        ('independent', 'Independent worker'),
        ('job_seeker', 'Job seeker'),
        ('education', 'In education or in training'),
        ('unknow', 'End unknow'),
        ('withdrawal', 'Withdrawal')
        ],
        string="End type (priority 1,2,3,4)"
    )
    end_type_2 = fields.Selection([
        ('housing_support', 'Support and/or access to adapted and/or inclusive housing'),
        ('social_support', 'Support for social inclusion / access to leisure activities'),
        ('self_help_support', 'Self-help/self-care support'),
        ('mobility_support', 'Mobility support'),
        ('new_skills', 'Acquire new skills/capacities/abilities to better support/help target audiences'),
        ('unknow', 'Unknow'),
        ('withdrawal', 'Withdrawal')
        ],
        string="End type (priority 5)"
    )
    aquired = fields.Selection([
        ('recognized_qualification', 'Obtaining a recognized qualification'),
        ('achivement_cert', 'Certificate of achievement'),
        ('participation_cert', 'Certificate of participation'),
        ('not_applicable', 'Not applicable')
        ],
        string="Achievements at end of action"
    )
    comments = fields.Char(string="Comments")
    ineligble_AFSE = fields.Boolean(string="participant made ineligible by AFSE")
    comments_afse = fields.Char(string="Comments AFSE")
    ineligibility_reason = fields.Char(string="Reason for ineligibility")
