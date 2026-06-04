from odoo import models, fields, api
from datetime import date


class HospitalVisit(models.Model):
    """Model representing a patient visit in the hospital system."""

    _name = 'hr.hospital.visit'
    _description = 'Patient Visits'
    _order = 'planned_datetime desc'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )

    status = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Visit Status',
        default='planned'
    )

    planned_datetime = fields.Datetime(
        string='Planned Visit Date & Time',
        required=True
    )

    visit_datetime = fields.Datetime(
        string='Visit Date & Time'
    )

    visit_count = fields.Integer(
        string="Count",
        default=1
    )

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Doctor',
        required=True
    )

    patient_id = fields.Many2one(
        'hr.hospital.patient',
        string='Patient',
        required=True
    )

    summary = fields.Html(
        string='Epicrisis / Summary'
    )

    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Diagnosis'
    )

    is_locked = fields.Boolean(
        compute='_compute_is_locked',
        store=False
    )

    @api.depends('visit_datetime')
    def _compute_is_locked(self):
        """Determine whether the visit record is locked based on visit date."""
        for rec in self:
            if not rec.id:
                rec.is_locked = False
                continue

            if rec.visit_datetime:
                visit_date = fields.Date.to_date(rec.visit_datetime)
                today = fields.Date.context_today(rec)

                rec.is_locked = visit_date <= today
            else:
                rec.is_locked = False

    @api.depends('patient_id', 'doctor_id', 'visit_datetime')
    def _compute_name(self):
        """Compute visit display name based on patient, doctor, and datetime."""
        for rec in self:
            patient = rec.patient_id.name or ''
            doctor = rec.doctor_id.name or ''
            visit_datetime = rec.visit_datetime or ''

            rec.name = f"{patient} - {doctor} - {visit_datetime}"