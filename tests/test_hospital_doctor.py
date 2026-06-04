from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestHospitalDoctor(TransactionCase):

    def setUp(self):
        super().setUp()

        self.category = self.env['hr.hospital.doctor.category'].create({
            'name': 'Therapist',
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Dr. House',
            'category_id': self.category.id,
        })

        self.mentor = self.env['hr.hospital.doctor'].create({
            'name': 'Dr. Mentor',
            'category_id': self.category.id,
        })


    def test_is_intern_compute(self):
        intern = self.env['hr.hospital.doctor'].create({
            'name': 'Intern Doc',
            'category_id': self.category.id,
            'mentor_id': self.mentor.id,
        })

        self.assertTrue(intern.is_intern)
        self.assertEqual(intern.mentor_id.id, self.mentor.id)


    def test_mentor_constraint(self):
        intern = self.env['hr.hospital.doctor'].create({
            'name': 'Bad Intern',
            'category_id': self.category.id,
            'mentor_id': self.mentor.id,
        })

        with self.assertRaises(ValidationError):
            intern.mentor_id = intern
            intern._check_mentor()

