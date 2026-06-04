from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestDoctorCategory(TransactionCase):

    def setUp(self):
        super().setUp()

    def test_sequence_auto_set(self):
        cat1 = self.env['hr.hospital.doctor.category'].create({
            'name': 'Therapy',
        })

        cat2 = self.env['hr.hospital.doctor.category'].create({
            'name': 'Surgery',
        })

        self.assertTrue(cat1.sequence > 0)
        self.assertTrue(cat2.sequence > cat1.sequence)

    def test_unique_name_constraint(self):
        self.env['hr.hospital.doctor.category'].create({
            'name': 'Unique Category',
        })

        with self.assertRaises(ValidationError):
            self.env['hr.hospital.doctor.category'].create({
                'name': 'Unique Category',
            })