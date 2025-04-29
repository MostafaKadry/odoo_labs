from odoo import fields, models

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"

    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string="Gender", required=True)
    specialization = fields.Char(string="Specialization")
    phone = fields.Char(string="Phone")
    image = fields.Binary(string='Patient Image', attachment=True)

    patient_ids = fields.Many2many(
        'hospital.patient',
        string='Assigned Patients'
    )