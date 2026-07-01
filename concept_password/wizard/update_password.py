import datetime
from odoo import api, fields, models, _ 
from odoo.exceptions import ValidationError



class UpdatePasswordWizard(models.TransientModel):
    _name = "update.password.wizard"
    _description = "Update Password Wizard"
    
    
    
    @api.model
    def default_get(self, fields):
        res=super(UpdatePasswordWizard,self).default_get(fields)
        res['acitve_id']= self.env.context.get('active_id')
        res["customer_name"]= self.env.context.get('customer_name')
        password_record = self.env['device.list.lines'].with_context(active_test=False).search([('id', '=', res['acitve_id'])], limit=1)
        # raise ValidationError(_(password_record.device_id.name))
        res.update({
                    # 'device_id': password_record.device_id.name,
                    'user_name': password_record.user_name,
                    'name': password_record.name,
                    'ip_name': password_record.ip_name,
                    'password_name': password_record.password_name,
                    'description': password_record.description,
                    # 'password_form_id': password_record.id,
                })
        return res
    
    
    acitve_id = fields.Char(string="Record ID")
    device_id = fields.Many2one('device.list')
    user_name = fields.Char(string="User Name")
    name = fields.Char(string="Name")
    ip_name = fields.Char(string="IP")
    password_name = fields.Char(string="Password")
    description = fields.Text(string="Descrition")
    customer_name=fields.Many2one('password.form', string='Customer name')
    
    # partner_id = fields.Many2one(
    #     'res.partner',
    #     string="Customer",
    #     related='password_form_id.partner_id',
    #     store=True,
    #     readonly=True
    # )
    

   
    
    # appointment_id=fields.Many2one('hospital.appointment', string="Appointment", domain=[('state', '=', 'draft')])
    # reason=fields.Text(string="Reason")
    # date_cancel=fields.Date(string='Booking Date', default=fields.Date.context_today)

    def action_update(self):
       
        record = self.env['device.list.lines'].with_context(active_test=False).search(
            [('id', '=', self.acitve_id)], limit=1 )

        # raise ValidationError(_("Record Found: ID=%s") % (record))
        record.write({
            'user_name': self.user_name,
            'name': self.name,
            'ip_name': self.ip_name,
            'password_name': self.password_name,
            'description': self.description,
        })

        return {'type': 'ir.actions.act_window_close'}
        