from odoo import models, fields, api


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Новий Лікар',
        required=True
    )

    change_date = fields.Date(
        string='Дата зміни',
        default=fields.Date.today
    )

    def action_apply(self):
        active_ids = self.env.context.get('active_ids', [])
        patients = self.env['hr.hospital.patient'].browse(active_ids)

        patients.write({
            'doctor_id': self.doctor_id.id,
            'doctor_change_date': self.change_date
        })

