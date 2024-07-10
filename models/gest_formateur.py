from odoo import models,fields,api


class GestFormateur(models.Model):
    _name= 'gest.formateur'

    matricule = fields.Integer()
    name = fields.Char()
    diplome = fields.Char()
    session = fields.Many2many('gest.session')

    _sql_constraints = [
        ('formateur_unique', 'unique(matricule)', 'formateur existe ')
    ]





