# -*- coding: utf-8 -*-
{
    'name': 'teamdoo_gestion_formation',

    # Categories can be used to filter modules in modules listing
    'version': '17.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gestion_formation.xml',
        'views/gestion_formateur.xml',
        'views/gestion_session.xml',
        'views/gestion_salle.xml',
        'views/gestion_candidat.xml',
    ],

    'demo': [
        # 'demo/demo.xml',
    ],

    'application': True,
    'installable': True,

}
