from odoo.tests.common import TransactionCase


class TestHospitalPatient(TransactionCase):

    def setUp(self):
        super().setUp()

        self.doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Dr. House'
        })

    # -----------------------
    # TEST 1: patient create
    # -----------------------
    def test_patient_creation(self):
        patient = self.env['hr.hospital.patient'].create({
            'name': 'John Doe',
            'phone': '123456',
            'doctor_id': self.doctor.id,
        })

        self.assertEqual(patient.name, 'John Doe')
        self.assertEqual(patient.doctor_id, self.doctor)

    # -----------------------
    # TEST 2: action returns dict
    # -----------------------
    def test_action_create_quick_visit(self):
        patient = self.env['hr.hospital.patient'].create({
            'name': 'Jane Doe',
            'doctor_id': self.doctor.id,
        })

        action = patient.action_create_quick_visit()

        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'hr.hospital.visit')
        self.assertEqual(action['view_mode'], 'form')
        self.assertIn('default_patient_id', action['context'])