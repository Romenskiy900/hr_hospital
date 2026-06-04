from odoo import models, fields, api


class HospitalDoctorCategory(models.Model):
    """
    Doctor Category model.

    Stores categories for doctors with sequence ordering and uniqueness constraint.
    Used to group doctors and control display order in the system.
    """
    _name = 'hr.hospital.doctor.category'
    _description = 'Doctor Categories'
    _order = 'sequence, name'
    _inherit = ['sequence.mixin', 'unique.field.mixin']

    name = fields.Char(string='Category', required=True)

    sequence = fields.Integer(
        string='Sequence',
        readonly=True,
        copy=False
    )

    doctor_ids = fields.One2many(
        'hr.hospital.doctor',
        'category_id',
        string='Doctors'
    )

    def create(self, vals):
        """
        Overrides create to:
        - assign sequence automatically
        - enforce unique category name
        """
        if not self._context.get('install_mode'):
            vals = self._check_and_set_sequence(
                vals,
                'sequence'
            )
            vals = self._check_unique_field_mixin(
                vals,
                'name'
            )
        return super().create(vals)

    def write(self, vals):
        """
        Ensures category name uniqueness on update.
        """
        if 'name' in vals:
            for rec in self:
                rec._check_unique_field_mixin(vals, 'name')

        return super().write(vals)