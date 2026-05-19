# Copyright 2025 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FSETimeLogCleanupWizard(models.TransientModel):
    _name = 'fse.time.log.cleanup.wizard'
    _description = 'Cleanup duplicate FSE Time Log entries'

    line_ids = fields.One2many(
        'fse.time.log.cleanup.line',
        'wizard_id',
        string='Duplicates found',
    )
    state = fields.Selection(
        [('detect', 'Detect'), ('done', 'Done')],
        default='detect',
    )
    duplicate_count = fields.Integer(
        compute='_compute_duplicate_count',
    )

    @api.depends('line_ids')
    def _compute_duplicate_count(self):
        for wizard in self:
            wizard.duplicate_count = len(wizard.line_ids)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        duplicates = self._find_duplicates()
        if not duplicates:
            raise UserError(_('No duplicate FSE Time Log entries found.'))
        res['line_ids'] = [(0, 0, vals) for vals in duplicates]
        return res

    def _find_duplicates(self):
        """Detect duplicate fse.time.log records per (partner_id, year).

        For each group with more than one record, keep the oldest (MIN id)
        and mark all others as duplicates to delete.
        """
        self.env.cr.execute("""
            SELECT ftl.id, ftl.partner_id, ftl.year,
                   ftl.time_fse_p1, ftl.time_fse_p2
            FROM fse_time_log ftl
            WHERE ftl.id NOT IN (
                SELECT MIN(id)
                FROM fse_time_log
                GROUP BY partner_id, year
            )
            ORDER BY ftl.partner_id, ftl.year
        """)
        rows = self.env.cr.dictfetchall()
        return [
            {
                'fse_time_log_id': row['id'],
                'partner_id': row['partner_id'],
                'year': row['year'],
                'time_fse_p1': row['time_fse_p1'],
                'time_fse_p2': row['time_fse_p2'],
            }
            for row in rows
        ]

    def action_delete_duplicates(self):
        """Delete all detected duplicate records."""
        self.ensure_one()
        log_ids = self.line_ids.mapped('fse_time_log_id')
        if not log_ids:
            raise UserError(_('No duplicates to delete.'))
        count = len(log_ids)
        log_ids.unlink()
        self.state = 'done'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Cleanup complete'),
                'message': _('%d duplicate FSE Time Log entries deleted.') % count,
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            },
        }


class FSETimeLogCleanupLine(models.TransientModel):
    _name = 'fse.time.log.cleanup.line'
    _description = 'FSE Time Log Cleanup Line'

    wizard_id = fields.Many2one(
        'fse.time.log.cleanup.wizard',
        required=True,
        ondelete='cascade',
    )
    fse_time_log_id = fields.Many2one(
        'fse.time.log',
        string='Duplicate entry',
        required=True,
        ondelete='cascade',
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        readonly=True,
    )
    year = fields.Char(readonly=True)
    time_fse_p1 = fields.Float(
        string='Temps FSE P1',
        readonly=True,
    )
    time_fse_p2 = fields.Float(
        string='Temps FSE P2',
        readonly=True,
    )
