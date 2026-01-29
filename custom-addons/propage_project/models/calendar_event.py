from odoo import api, fields, models


class Meeting(models.Model):
    _inherit = 'calendar.event'

    time_registered = fields.Boolean()
