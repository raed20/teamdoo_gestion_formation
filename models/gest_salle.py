from odoo import models,fields


class GestSalle(models.Model):
    _name='gest.salle'

    name = fields.Char()
    nbre_place = fields.Integer()
    libre = fields.Boolean()
    sessionId = fields.Many2many('gest.session')
    salleref = fields.Integer()
    _sql_constraints = [
        ('classroom_ref_unique', 'unique(salleref)', 'classroom reference exist'),
        ('classroom_name_unique', 'unique(name)', 'classroom name exist')
    ]

