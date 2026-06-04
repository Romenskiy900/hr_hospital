from dateutil.utils import today

from odoo import models, fields


class HospitalPatient(models.Model):
    """Model representing a hospital patient."""

    _name = 'hr.hospital.patient'
    _description = 'Patient'

    _inherit = ['hospital.medic.info']

    name = fields.Char(string='Full Name', required=True)

    phone = fields.Char(string='Phone')

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Personal Doctor'
    )

    history_ids = fields.One2many(
        'hr.hospital.doctor.history',
        'patient_id',
        string='Doctor History'
    )

    insurance_number = fields.Char(
        string='Insurance Policy Number',
        size=20
    )

    user_id = fields.Many2one('res.users')

    doctor_change_date = fields.Date(string="Doctor Change Date")

    def action_open_patient_visits(self):
        """Open patient visit history view."""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit History',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_quick_visit(self):
        """Create a new visit record with prefilled patient data."""
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'New Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
                'default_visit_datetime': today(),
                'default_planned_datetime': today(),
            }
        }