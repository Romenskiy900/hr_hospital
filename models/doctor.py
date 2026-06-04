from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    """
    Hospital Doctor model.

    Stores information about doctors, their category, mentor-intern relations,
    assigned patients and visit history.
    """
    _name = 'hr.hospital.doctor'
    _description = 'Лікар'

    name = fields.Char(string='Full Name', required=True)

    category_id = fields.Many2one(
        'hr.hospital.doctor.category',
        string='Category'
    )

    user_id = fields.Many2one(
        'res.users',
        string='System User'
    )

    mentor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='Mentor',
        domain=[('is_intern', '=', False)]
    )

    is_intern = fields.Boolean(
        string='Intern',
        compute='_compute_is_intern',
        store=True
    )

    intern_ids = fields.One2many(
        'hr.hospital.doctor',
        'mentor_id',
        string='Interns'
    )

    visit_ids = fields.One2many(
        'hr.hospital.visit',
        'doctor_id',
        string='Visit History'
    )

    patient_ids = fields.Many2many(
        'hr.hospital.patient',
        compute='_compute_patient_ids',
        string='Doctor Patients'
    )

    @api.depends('visit_ids.patient_id')
    def _compute_patient_ids(self):
        """
        Computes all patients linked to doctor via visits.
        """
        for rec in self:
            rec.patient_ids = rec.visit_ids.mapped('patient_id')

    @api.depends('mentor_id')
    def _compute_is_intern(self):
        """
        Determines if doctor is intern based on mentor assignment.
        """
        for rec in self:
            rec.is_intern = bool(rec.mentor_id)

    @api.constrains('mentor_id')
    def _check_mentor(self):
        """
        Validates mentor relationship.

        Rules:
        - Mentor cannot be an intern
        - A doctor who already supervises interns cannot become an intern
        """
        for rec in self:
            if rec.mentor_id:
                if rec.mentor_id.is_intern:
                    raise ValidationError('Mentor cannot be an intern')
                else:
                    interns = self.search([
                        ('mentor_id', '=', rec.id),
                        ('is_intern', '=', True)
                    ], limit=1)

                    if interns:
                        raise ValidationError(
                            'This doctor is already a mentor and cannot be an intern'
                        )

    def action_create_visit(self):
        """
        Opens wizard/form to create a new visit for selected doctor.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id
            }
        }