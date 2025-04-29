{
    'name': 'Hospital Management',
    'version': '1.0',
    'author': 'Mostafa K.',
    'summary': 'Manage hospital patients, doctors, and departments',
    'category': 'Healthcare',
    'depends': ['base'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_views.xml',
        'views/patient_log_views.xml',
        'reports/patient_report.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
