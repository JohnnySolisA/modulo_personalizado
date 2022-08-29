# -*- coding:utf-8 -*-

{
    'name' : 'Módulo Personalizado',
    'version' : '1.1',
    'depends' : [
        'contacts',
        'mail',
    ],
    'author' : 'Johnny Solis',
    'website' : 'http://google.com',
    'summary' : 'Sumario Personalizado ODOO',
    'category' : 'Categoria Personalizada',
    'description' : 'Descripción Personalizada',
    'data' : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/update_wizard_view.xml',
        'data/categoria.xml',
        'data/secuencias.xml',
        'views/menu.xml',
        'views/presupuesto_view.xml',
        'views/res_partner_inherit.xml',
        'report/reporte_pelicula.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'modulo_personalizado/static/src/css/style.css',
        ],
        'web.assets_qweb': [
            'modulo_personalizado/static/src/xml/button_accion.xml',
        ],
    }
}
