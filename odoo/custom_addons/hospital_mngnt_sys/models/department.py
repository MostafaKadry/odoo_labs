from odoo import models, fields, api


class HospitalDepartment(models.Model):
    _name = "hospital.department"
    _description = "Hospital Department"

    name = fields.Char(string="Department Name", required=True)
    capacity = fields.Integer(string="Bed Capacity")
    is_opened = fields.Boolean(string="Is Opened?", default=True)
    patient_ids = fields.One2many(
        'hospital.patient',
        'department_id',
        string="Patients"
    )
    current_occupancy = fields.Integer(
        string='Occupancy',
        compute='_compute_occupancy'
    )

    @api.depends('patient_ids')
    def _compute_occupancy(self):
        for dept in self:
            dept.current_occupancy = len(dept.patient_ids)