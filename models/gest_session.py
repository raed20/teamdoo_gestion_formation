from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GestSession(models.Model):
    _name = 'gest.session'

    name = fields.Char()
    nbre_participants = fields.Integer()
    date_debut = fields.Datetime()
    date_fin = fields.Datetime()
    duree = fields.Char(string='duree', compute='compute_duree')
    status = fields.Selection([
        ('on hold', 'on hold'),
        ('off', 'off'),
        ('on', 'on'),
    ], string='Select Option', required=True, default='off')
    color = fields.Integer()
    formation_id = fields.Many2one('gest.formation', string='Formation', ondelete="cascade")
    salle_ids = fields.Many2many('gest.salle', 'session_salle_rel', string='Salles')
    candidat_ids = fields.Many2many('gest.candidat', 'session_candidat_rel', string='Candidats')
    formateur_ids = fields.Many2many('gest.formateur', 'session_formateur_rel', string='Formateurs')

    @api.depends('date_debut', 'date_fin')
    def compute_duree(self):
        for session in self:
            if session.date_debut and session.date_fin and session.verif_date():
                delta = session.date_fin - session.date_debut
                session.duree = str(delta)
            else:
                session.duree = False

    def verif_date(self):
        for session in self:
            if session.date_debut and session.date_fin:
                if session.date_debut > session.date_fin:
                    print('date debut must be lower than date fin')
                    return False
                else:
                    return True
            else:
                return False

    @api.constrains('date_debut', 'date_fin', 'salle_ids', 'nbre_participants')
    def check_salle_available(self):
        for session in self:
            if session.date_debut and session.date_fin and session.salle_ids:
                salle_ids = session.salle_ids.ids
                overlapping_sessions = self.env['gest.session'].search([
                    ('id', '!=', session.id),
                    ('salle_ids', 'in', salle_ids),
                    ('date_debut', '<=', session.date_fin),
                    ('date_fin', '>=', session.date_debut)
                ])
                if overlapping_sessions:
                    raise ValidationError("La salle sélectionnée n'est pas available pour cette période.")
                for salle in session.salle_ids:
                    if session.nbre_participants > salle.nbre_place:
                        raise ValidationError(
                            f"La salle {salle.name} n'a pas assez de places availables pour le nombre de participants ({session.nbre_participants}).")

    @api.constrains('date_debut', 'date_fin', 'formateur_ids')
    def check_formateur_available(self):
        for session in self:
            if session.date_debut and session.date_fin and session.formateur_ids:
                formateur_ids = session.formateur_ids.ids
                overlapping_sessions = self.env['gest.session'].search([
                    ('id', '!=', session.id),
                    ('formateur_ids', 'in', formateur_ids),
                    ('date_debut', '<=', session.date_fin),
                    ('date_fin', '>=', session.date_debut)
                ])
                if overlapping_sessions:
                    raise ValidationError("Le formateur sélectionné n'est pas available pour cette période.")

    @api.constrains('date_debut', 'date_fin', 'candidat_ids')
    def check_candidat_available(self):
        for session in self:
            if session.date_debut and session.date_fin and session.candidat_ids:
                candidat_ids = session.candidat_ids.ids
                overlapping_sessions = self.env['gest.session'].search([
                    ('id', '!=', session.id),
                    ('candidat_ids', 'in', candidat_ids),
                    ('date_debut', '<=', session.date_fin),
                    ('date_fin', '>=', session.date_debut)
                ])
                if overlapping_sessions:
                    raise ValidationError("Le candidat sélectionné n'est pas available pour cette période.")

    @api.constrains('candidat_ids')
    def check_nbre_participants(self):
        for session in self:
            if len(session.candidat_ids) > session.nbre_participants:
                raise ValidationError(
                    f"Le nombre de candidats inscrits ({len(session.candidat_ids)}) "
                    f"dépasse le nombre de participants autorisés ({session.nbre_participants}).")


    def action_delete_session(self):
        for session in self:
            session.unlink()
        return True

    @api.model
    def create(self, vals):
        session = super(GestSession, self).create(vals)
        session._update_salle_status()
        return session

    def write(self, vals):
        res = super(GestSession, self).write(vals)
        self._update_salle_status()
        return res

    def unlink(self):
        sessions = self
        res = super(GestSession, sessions).unlink()
        self._update_salle_status()
        return res

    def _update_salle_status(self):
        salle = self.env['gest.salle']
        now = fields.Datetime.now()
        all_salles = salle.search([])
        all_salles.write({'libre': True})

        current_sessions = self.search([
            ('date_debut', '<=', now),
            ('date_fin', '>=', now),
        ])
        for session in current_sessions:
            session.salle_ids.write({'libre': False})

    def action_join_session(self):
        active_candidat_id = self.env.context.get('active_candidat_id')
        if not active_candidat_id:
            raise ValidationError("No candidate selected.")
        if active_candidat_id in self.candidat_ids.ids:
            raise ValidationError("The candidate is already enrolled in this session.")
        current_participant_count = len(self.candidat_ids)
        if current_participant_count >= self.nbre_participants:
            raise ValidationError("This session is full.")

        self.write({
            'candidat_ids': [(4, active_candidat_id)]
        })


        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ("successfully joined"),

                'type': 'success',
                'message': ("Congrats ! you successfully joined the session"),

                'sticky': True,
            },
        }

    _sql_constraints = [
        ('check_date', 'CHECK(date_debut < date_fin)', 'Start date must be before end date')
    ]

