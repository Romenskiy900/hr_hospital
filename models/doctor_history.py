from odoo import models, fields, api


class HospitalDoctorHistory(models.Model):
    """Model for storing history of doctor assignments to patients."""

    _name = 'hr.hospital.doctor.history'
    _description = 'Personal Doctor History'
    _order = 'date_start desc'
    _inherit = ['sequence.mixin']

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )
    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True
    )

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True
    )

    date_start = fields.Date(
        string='Assignment Date',
        default=fields.Date.today
    )

    date_end = fields.Date(
        string='Doctor Change Date',
        default=fields.Date.today
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    @api.onchange('date_start', 'date_end')
    def _onchange_dates(self):
        """Validate that end date is not earlier than start date."""
        if self.date_start and self.date_end:
            if self.date_end < self.date_start:
                self.date_end = self.date_start
                return {
                    'warning': {
                        'title': 'Date Error',
                        'message': 'Doctor change date cannot be earlier than assignment date'
                    }
                }

    @api.depends('patient_id', 'doctor_id', 'doctor_id.category_id', 'date_start')
    def _compute_name(self):
        """Compute record display name based on patient, doctor and date."""
        for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            category = rec.doctor_id.category_id.name or ''
            date = rec.date_start or ''

            rec.name = f"{patient} - {doctor} ({category}) {date}"