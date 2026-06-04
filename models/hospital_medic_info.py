from odoo import models, fields, api


class HospitalMedicInfo(models.AbstractModel):
    """Abstract model that stores common medical information fields."""

    _name = 'hospital.medic.info'
    _description = 'Medical Information'

    blood_group = fields.Selection(
        selection=[
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string='Blood Group'
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        string='Gender'
    )

    birth_date = fields.Date(string='Birth Date')

    age = fields.Integer(string='Age')

    @api.onchange('birth_date')
    def _onchange_birth_date(self):
        """Recalculate age based on birth date."""
        for rec in self:
            if rec.birth_date:
                today = fields.Date.context_today(rec)
                birth = fields.Date.to_date(rec.birth_date)
                change_year = -1
                if today.month > birth.month or (today.month == birth.month and today.day >= birth.day):
                    change_year = 0
                rec.age = today.year - birth.year + change_year
            else:
                rec.age = 0