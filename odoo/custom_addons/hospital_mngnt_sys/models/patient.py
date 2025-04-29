import re
from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _order = 'create_date desc'

    # Basic Info
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(
        string="Email",
        help="Patient's email address",
    )

    # Medical Info
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Blood Type')
    cr_ratio = fields.Float(string='CR Ratio')
    pcr = fields.Boolean(string='PCR Tested')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='Status', default='undetermined')
    medical_history = fields.Html(string='Medical History')
    department_id = fields.Many2one(
        'hospital.department',
        string="Assigned Department"
    )
    doctor_ids = fields.Many2many(
        'hospital.doctor',
        string='Assigned Doctors'
    )
    department_capacity = fields.Integer(
        string='Department Capacity',
        related='department_id.capacity',
        store=True,
        readonly=True
    )

    # Additional Info
    address = fields.Text(string='Address')
    image = fields.Binary(string='Patient Image', attachment=True)

    log_ids = fields.One2many(
        'hospital.patient.log',
        'patient_id',
        string='History Logs'
    )

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                age = today.year - record.birth_date.year
                if (today.month, today.day) < (record.birth_date.month, record.birth_date.day):
                    age -= 1
                record.age = age
            else:
                record.age = 0

    def action_add_log(self):
        return {
            'name': 'Add Patient Log',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient.log',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
            }
        }

    @api.model
    def create(self, vals):
        record = super(HospitalPatient, self).create(vals)
        record._create_log('Patient record created')
        return record

    def write(self, vals):
        # Handle state change logging
        if 'state' in vals:
            for patient in self:
                patient._create_log(
                    f"State changed to {vals['state'].title()}",
                    log_type='status'
                )
        # Handle general update logging
        if vals:  # Only log if there are actual changes
            for patient in self:
                patient._create_log('Patient record updated')
        return super(HospitalPatient, self).write(vals)

    def _create_log(self, message, log_type='info'):
        self.ensure_one()
        return self.env['hospital.patient.log'].create({
            'patient_id': self.id,
            'description': message,
            'type': log_type
        })

    def action_set_good(self):
        self.write({'state': 'good'})

    def action_set_fair(self):
        self.write({'state': 'fair'})

    def action_set_serious(self):
        self.write({'state': 'serious'})

    def action_reset(self):
        self.write({'state': 'undetermined'})

    @api.constrains('email')
    def _check_valid_email(self):
        for patient in self:
            if patient.email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', patient.email):
                raise ValidationError("Please enter a valid email address (e.g., patient@example.com)")

    _sql_constraints = [
        (
            'email_unique',
            'UNIQUE(email)',
            'Email address must be unique!',
        ),
    ]