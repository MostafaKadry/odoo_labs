from odoo import models, fields


class User(models.Model):
    _name = 'todo.user'
    _description = 'User'

    name = fields.Char(required=True)
    join_date = fields.Datetime(default=fields.Datetime.now)
    avatar = fields.Binary()
    is_active = fields.Boolean



