from odoo import fields, models


class TimesheetsAnalysisReport(models.Model):
    _inherit = "timesheets.analysis.report"

    customer_id = fields.Many2one('res.partner', string='Customer', readonly=True)

    def _select(self):
        return super()._select() + ", A.customer_id"

    def _group_by(self):
        return super()._group_by() + ", A.customer_id"
