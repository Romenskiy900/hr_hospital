from odoo import models, fields


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Лікарі')
    patient_ids = fields.Many2many('hr.hospital.patient', string='Пацієнти')

    date_from = fields.Date(string='Початок періоду')
    date_to = fields.Date(string='Кінець періоду')

    only_done = fields.Boolean(string='Лише завершені візити')

    disease_id = fields.Many2one(
        'hr.hospital.disease',
        string='Хвороба'
    )

    def action_generate(self):
        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))

        if self.date_from:
            domain.append(('visit_datetime', '>=', self.date_from))

        if self.date_to:
            domain.append(('visit_datetime', '<=', self.date_to))

        if self.only_done:
            domain.append(('status', '=', 'done'))

        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
        }