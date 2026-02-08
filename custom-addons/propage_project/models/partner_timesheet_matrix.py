from odoo import models, fields


class PartnerTimesheetMatrix(models.Model):
    _name = 'partner.timesheet.matrix'
    _description = "timesheet matrix"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    task_id = fields.Many2one('project.task', string="Task")
    year = fields.Char(string="Year")
    amount = fields.Float(string="Hours")
