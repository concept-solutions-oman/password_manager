from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class PasswordForm(models.Model):
    _name = "password.form"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Password Form"
    _rec_name = 'partner_id'
    
    _sql_constraints = [
        ('partner_id_uniq', 'unique (partner_id)', 'A password form for this customer already exists!')
    ]

    partner_id = fields.Many2one('res.partner', string="Customer",  required=True, tracking=True)   
    active = fields.Boolean(default=True, Tracking=True)
    device_password_ids=fields.One2many('device.list.lines','password_form_id',  string='Password Lines')
    responsible_user_ids = fields.Many2many('res.users', string="Responsible Persons", tracking=True)
    password_count = fields.Integer(string="Passwords", compute='_compute_password_count')
    device_ids = fields.Many2many('device.list', string='Devices', compute='_compute_device_ids', store=True)

    @api.depends('device_password_ids.device_id')
    def _compute_device_ids(self):
        for record in self:
            record.device_ids = record.device_password_ids.mapped('device_id')

    @api.depends('device_password_ids')
    def _compute_password_count(self):
        for record in self:
            record.password_count = len(record.device_password_ids)

    @api.onchange('partner_id')
    def password_availability(self):
        password_record = self.env['password.form'].with_context(active_test=False).search([('partner_id', '=', self.partner_id.id)])
        if password_record:
            raise ValidationError(
                        f"Password already exists for this Customer ")



class DeviceListLines(models.Model):
    _name = "device.list.lines"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Device List Lines"

    device_id = fields.Many2one('device.list', string="Device/Applications")
    user_name = fields.Char(string="User Name",tracking=True)
    name = fields.Char(string="Name",tracking=True)
    ip_name = fields.Char(string="IP",tracking=True)
    url = fields.Char(string="URL/Link", tracking=True)
    password_name = fields.Char(string="Password", tracking=True)
    description = fields.Text(string="Description")
    password_form_id = fields.Many2one('password.form', string='Password Form', required=False)
    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        store=True,
    )
    responsible_user_ids = fields.Many2many('res.users', string="Responsible Persons", tracking=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            # Find existing form for this customer
            form = self.env['password.form'].sudo().search([('partner_id', '=', self.partner_id.id)], limit=1)
            if not form:
                # If no form exists, we will create one (or suggest creating one)
                # For onchange, we can prepare the creation context or just create it?
                # Creating in onchange is bad practice.
                # Better: Leave it empty, but handle in create/write?
                # Or just create it now? No, onchange shouldn't commit.
                # Let's just try to find it.
                pass
            else:
                self.password_form_id = form.id
        else:
            self.password_form_id = False

    @api.model
    def create(self, vals):
        if vals.get('partner_id') and not vals.get('password_form_id'):
            # Check if form exists
            partner_id = vals.get('partner_id')
            form = self.env['password.form'].sudo().search([('partner_id', '=', partner_id)], limit=1)
            if not form:
                # Create new form
                form = self.env['password.form'].create({'partner_id': partner_id})
            vals['password_form_id'] = form.id
        return super(DeviceListLines, self).create(vals)
    
    @api.constrains('ip_name')
    def _check_valid_ip(self):
        ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
        for record in self:
            if record.ip_name and not re.match(ip_pattern, record.ip_name):
                raise ValidationError("Please enter a valid IPv4 address (e.g. 192.168.1.1).")
            if record.ip_name:
                parts = record.ip_name.split(".")
                for part in parts:
                    if int(part) < 0 or int(part) > 255:
                        raise ValidationError("Each part of IP must be between 0 and 255.")
                    
                    
    # def action_send_message(self):
        
    #     raise ValidationError("Each part of IP must be between 0 and 255.")
    

    
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Device Password Lines',
        #     'res_model': 'device.list.lines',
        #     'view_mode': 'tree',  
        #     'target': 'current',
        #     'domain': [('partner_id', '=', self.partner_id.id)]
        # 	}
        