# -*- coding:utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class UpdateWizard(models.TransientModel):
    _name = "update.wizard"
    _description = "Actualizar Wizard"

    name = fields.Text(string="Nieva Descripción")
    archivo = fields.Binary()
    filename_archivo = fields.Char(string="Nombre del Archivo")

    def update_vista_general(self):
        if self.filename_archivo:
            if '.pdf' not in self.filename_archivo:
                raise ValidationError("El archivo debe ser un PDF")
        presupuesto_obj = self.env['presupuesto']
        #presupuesto_id = presupuesto_obj.search([('id', '=', self._context['active_id'])])
        presupuesto_id = presupuesto_obj.browse(self._context['active_id'])
        presupuesto_id.general = self.name