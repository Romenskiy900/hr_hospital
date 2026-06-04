{
    'name': 'Лікарняний облік',
    'version': '19.0.1.0.0',
    'category': 'Охорона здоров’я',
    'summary': 'Модуль для автоматизації лікарні',
    'depends': ['base'],
    'data': [

        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_rules.xml',
        'data/company_data.xml',


        'views/hr_hospital_doctor_search.xml',
        'views/doctor_views.xml',
        'views/disease_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml',
        'views/doctor_history_views.xml',
        'views/doctor_category_views.xml',
        'views/hr_hospital_actions.xml',
        'views/menu.xml',
        'wizard/mass_reassign_doctor_wizard_views.xml',
        'views/patient_actions.xml',
        'wizard/visit_report_wizard_views.xml',
        'views/visit_report_actions.xml',

        'views/hr_hospital_visit_calendar.xml',
        'views/hr_hospital_visit_search.xml',
        'views/hr_hospital_visit_pivot.xml',
        'views/hr_hospital_patient_search.xml',
        'report/doctor_report_template.xml',

    ],

    "demo": [
        "demo/demo_doctor_category_data.xml",
        "demo/demo_doctor.xml",
        "demo/demo_patient.xml",
        "demo/demo_disease.xml",
        "demo/demo_visit.xml",

    ],



    'installable': True,
    'auto_install': False,

}