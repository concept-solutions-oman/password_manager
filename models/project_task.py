# concept_project_task/models/project_task.py

from odoo import fields, models, api
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    password_access = fields.Many2many('res.users', string='Password access', 
                                      domain="[('id', 'in', user_ids)]",  tracking=True)
    can_see_password_button = fields.Boolean(
        compute="_compute_can_see_password_button"
    )
    task_status_button = fields.Boolean(
        compute="_compute_task_status_button"
    )
    password_record_count=fields.Integer(
        compute="_compute_task_status_button"
    )


    @api.depends('state')
    def _compute_task_status_button(self):
        for rec in self:
            if rec.partner_id:
                rec.password_record_count = self.env['device.list.lines'].search_count([
                    ('partner_id', '=', rec.partner_id.id)
                ])
            else:
                rec.password_record_count = 0
            if rec.state == "1_done" or rec.state == "1_canceled":
                rec.task_status_button = True
            else:
                rec.task_status_button = False



            
    @api.depends('password_access')
    def _compute_can_see_password_button(self):
        for rec in self:
            rec.can_see_password_button = self.env.user in rec.password_access

    def action_view_password(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Device Password Lines',
            'res_model': 'device.list.lines',
            'view_mode': 'tree',  
            'target': 'current',
            'domain': [('partner_id', '=', self.partner_id.id)]
        	}
        