from openerp import models, fields


class Step(models.Model):
    _name = 'release.step'

    filename = fields.Char(string="Filename", size=250, required=True)
