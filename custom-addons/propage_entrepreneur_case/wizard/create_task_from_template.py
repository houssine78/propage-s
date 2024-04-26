from odoo import fields, models


class create_task_wizard(models.TransientModel):
    _name = 'create.task.wizard'

    entrepreneur_case_id = fields.Many2one(
        'entrepreneur.case',
        string="Entrepreneur case",
        readonly=True
    )
    project_id = fields.Many2one(
        related='entrepreneur_case_id.project_id',
        readonly=True
    )
    task_ids = fields.Many2many(
        'project.task',
        string="tasks to create",
        domain=[('is_template', '=', True)]
    )

    def create_tasks(self):
        if not self.project_id:
            vals={
                'name': self.entrepreneur_case_id.name,
                'partner_id': self.entrepreneur_case_id.partner_id.id
            }
            project = self.env['project.project'].create(vals)
            self.entrepreneur_case_id.project_id = project.id
            
        for task in self.task_ids:
            task.copy(default={
                "project_id": self.entrepreneur_case_id.project_id.id,
                "entrepreneur_case_id": self.entrepreneur_case_id.id,
                "active": True,
            }
        )
        return {'type': 'ir.actions.act_window_close'}
