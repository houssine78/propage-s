from odoo import api, fields, models


class Meeting(models.Model):
    _name = 'meeting.type'

    code = fields.Char()
    name = fields.Char()
