from odoo import models, fields


class Task(models.Model):
    _name = 'todo.task'
    _description = 'Task'

    title = fields.Char(required=True)
    description = fields.Text()
    tag = fields.Char()
    image = fields.Binary()
    start_at = fields.Datetime()
    end_at = fields.Datetime()
    state = fields.Selection([('new', 'New'), ('doing','Doing'),('done', 'Done')], default='new')
