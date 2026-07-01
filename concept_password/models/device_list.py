from odoo import api, fields, models


class DeviceList(models.Model):
    _name = "device.list"
    _description = "Device List Names"

    name= fields.Char(String='Device Name', required=True, ondelete='restrict')
    active = fields.Boolean(default=True)

_sql_constraints = [
       ('unique_tag_name', 'unique (sequence)', 'Name not all')
   ]
    