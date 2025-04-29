from odoo import models, fields,api


class PatientLog(models.Model):
    _name = 'hospital.patient.log'
    _description = 'Patient Log History'
    _order = 'create_date desc'
    _rec_name = 'summary'

    patient_id = fields.Many2one('hospital.patient', required=True)
    user_id = fields.Many2one('res.users', string='By', default=lambda self: self.env.user)
    date = fields.Datetime(default=fields.Datetime.now, string='Date/Time')
    description = fields.Text(required=True)
    type = fields.Selection([
        ('info', 'Information'),
        ('treatment', 'Treatment'),
        ('note', 'Note'),
        ('status', 'Status Change')
    ], string='Type', default='info')

    summary = fields.Char(compute='_compute_summary', store=True)

    @api.depends('date', 'user_id', 'type')
    def _compute_summary(self):
        for log in self:
            log.summary = f"{log.date} - {log.user_id.name} - {log.type}"