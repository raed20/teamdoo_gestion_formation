from odoo import models , fields , api


class GestFormation(models.Model):
    _name = 'gest.formation'
    name = fields.Char()
    prix = fields.Float()
    formation_reference = fields.Integer("Reference")

    session = fields.One2many('gest.session', 'id')

    def action_view_sessions(self):
        return {
            'name': 'Sessions de la Formation',
            'type': 'ir.actions.act_window',
            'res_model': 'gest.session',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('formation_id', '=', self.id)],
        }

    _sql_constraints = [
        ('reference_formation_uniq', 'unique (formation_reference)', 'Reference must be unique per training.'),
    ]
