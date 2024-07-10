from odoo import models, fields, api


class GestCandidat(models.Model):
    _name = 'gest.candidat'

    name = fields.Char()
    email = fields.Char()
    session = fields.Many2many('gest.session')

    def action_view_formations(self):
        return {
            'name': 'Formations Disponibles',
            'type': 'ir.actions.act_window',
            'res_model': 'gest.formation',
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {'active_candidat_id': self.id},
        }