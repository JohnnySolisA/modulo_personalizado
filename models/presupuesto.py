# -*- coding:utf-8 -*-

import logging
import re
from odoo import fields, models, api
from odoo.exceptions import ValidationError,UserError

LOGGER = logging.getLogger(__name__)

class Presupuesto(models.Model):
    _name = "presupuesto"
    _description = "Presupuesto"
    _inherit = ['image.mixin','mail.thread','mail.activity.mixin']

    @api.depends('detalle_ids')
    def _compute_total(self):
        for rec in self:
            subtotal = 0
            for linea in rec.detalle_ids:
                subtotal += linea.importe
            rec.base = subtotal
            rec.impuestos = rec.base * 0.12
            rec.total = subtotal * 1.12

    name = fields.Char(string="Pelicula",required=True)
    clasificacion = fields.Selection(selection=[
        ('G','G'),
        ('PG','PG'),
        ('PG-13','PG-13'),
        ('R','R'),
        ('NC-17','NC-17'),
    ],string="Clasificación",required=True)
    desc_clas = fields.Char(string="Descripción Clasificación")
    fecha_estreno = fields.Date(string="Fecha de Estreno")
    puntuacion = fields.Integer(string="Puntuación",related="puntuacion_numero")
    puntuacion_numero = fields.Integer(string="Puntuación Numero")
    active = fields.Boolean(string="Activo",default=True)
    director_id = fields.Many2one(
        comodel_name='res.partner',
        string="Director"
    )
    categoria_director_id = fields.Many2one(
        comodel_name='res.partner.category',
        string="Categoría Director",
        default=lambda self: self.env.ref('modulo_personalizado.category_director')
        #default=lambda self: self.env['res.partner.category'].search([('name', '=', 'director')])
    )
    actores_id = fields.Many2many(
        comodel_name='res.partner',
        string="Actores"
    )
    categoria_actor_id = fields.Many2one(
        comodel_name='res.partner.category',
        string="Categoría Actor",
        default=lambda self: self.env.ref('modulo_personalizado.category_actor')
    )
    genero_ids = fields.Many2many(
        comodel_name='genero',
        string="Géneros"
    )
    general = fields.Text(string="Descripción")
    link_trailer = fields.Char(string="Trailer")
    es_libro = fields.Boolean(string="Version Libro")
    libro = fields.Binary(string="Libro")
    libro_filename = fields.Char(string="Nombre del Libro")
    state = fields.Selection(selection=[
        ('borrador','Borrador'),
        ('aprobado','Aprobado'),
        ('cancelado', 'Cancelado'),
    ],default='borrador',string="Estados",copy=False)
    fecha_creacion = fields.Datetime(string="Fecha de Creación", copy=False, readonly=True)
    fecha_aprobado = fields.Datetime(string="Fecha Aprobado",copy=False,readonly=True)
    num_presupuesto = fields.Char(string="Numero de Presupuesto",copy=False,readonly=True)
    opinion = fields.Html(string="Opinión")
    detalle_ids = fields.One2many(
        comodel_name='presupuesto.detalle',
        inverse_name='presupuesto_id',
        string="Detalle Ids"
    )
    campos_ocultos = fields.Boolean(string="Campos Ocultos")
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id.id,
        string="Moneda",
        readonly=True
    )
    terminos = fields.Text(string="Términos")
    base = fields.Monetary(string="Base Imponibe", compute='_compute_total')
    impuestos = fields.Monetary(string="Impuestos", compute='_compute_total')
    total = fields.Monetary(string="Total", compute='_compute_total')

    def aprobar_presupuesto(self):
        LOGGER.info('*************************BOTON APROBAR*************************')
        for rec in self:
            rec.state='aprobado'
            rec.fecha_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        for rec in self:
            rec.state = 'cancelado'

    def unlink(self):
        LOGGER.info('*************************FUNCION UNLINK*************************')
        for rec in self:
            if rec.state == 'cancelado':
                super(Presupuesto,rec).unlink()
            else:
                LOGGER.info('*************************NO SE PUEDE BORRAR*************************')
                raise UserError("No se puede Eliminar el registro porque no se encuentra en el estado CANCELADO")

    @api.model
    def create(self,variables):
        LOGGER.info('*************************VARIABLES: {0}'.format(variables))
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.pelicula')
        variables['num_presupuesto'] = correlativo
        variables['fecha_creacion'] = fields.Datetime.now()
        return super(Presupuesto,self).create(variables)

    #PARA VARIOS REGISTROS
    '''
    @api.model_create_multi
    def create(self, variables):
        return super(Presupuesto, self).create(variables)
    
    def crear_registro(self):
        registro1 = {
            'name' : self.name + "(Metodo de Creacion)",
            'num_presupuesto' : self.num_presupuesto+"----0000----",
        }
        registro2 = {
            'name': self.name + "(Metodo de Creacion)",
            'num_presupuesto': self.num_presupuesto + "----0000----",
        }
        self.env['presupuesto'].create([registro1,registro2])
    '''

    def write(self,variables):
        LOGGER.info('*************************VARIABLES: {0}'.format(variables))
        if 'clasificacion' in variables:
            raise UserError("La Clasificación no se puede modificar")
        return super(Presupuesto,self).write(variables)

    def copy(self,default=None):
        default = dict(default or {})
        default['name'] = self.name+" (copia)"
        return super(Presupuesto,self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.desc_clas = 'Público General'
            if self.clasificacion == 'PG':
                self.desc_clas = 'Se recomienda compañía de un adulto'
            if self.clasificacion == 'PG-13':
                self.desc_clas = 'En companía Obligatoria de un Adulto'
        else:
            self.desc_clas = False

    def toggle_state(self):
        self.es_libro = True

    def crear_registro(self):
        variable = {
            'name' : self.name + "(Metodo de Creacion)",
            'num_presupuesto' : self.num_presupuesto+"----0000----",
        }
        self.env['presupuesto'].create(variable)

    def actualizar_registro(self):
        variable = {
            'name': self.name + "(Metodo de Actualizacion)",
            'num_presupuesto': self.num_presupuesto + "----00100----",
        }
        id = self.env['presupuesto'].browse([self.id])
        id.write(variable)

    def eliminar_registro(self):
        id = self.env['presupuesto'].browse([self.id])
        id.unlink()

    @api.constrains('name')
    def validarName(self):
        for recorrido in self:
            if recorrido.name:
                if re.match(r"^[a-zA-Z][ a-zA-Z]*", recorrido.name):
                    raise ValidationError("El nombre solo debe contener NÚMEROS")

    def filter(self):
        presupuestos = self.env['presupuesto'].search([])
        presupuestos_filtered = presupuestos.filtered(lambda p: p.puntuacion >= 25)
        for rec in presupuestos_filtered:
            print(rec)

    def map(self):
        presupuestos = self.env['presupuesto'].search([])
        presupuestos_mapped = presupuestos.mapped(lambda p: p.puntuacion / 10)
        for rec in presupuestos_mapped:
            print(rec)

    def sort(self):
        presupuestos = self.env['presupuesto'].search([])
        presupuestos_sorted = presupuestos.sorted(key=lambda p: p.puntuacion,reverse=True)
        for rec in presupuestos_sorted:
            print(rec)

    def aplicar_sql(self):
        sql = "select id from presupuesto"
        self.env.cr.execute(sql)
        result = self.env.cr.fetchall()
        for rec in result:
            print(rec)

    def validate(self):
        if True:
            raise UserError("Se debe especificar")


class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"
    _description = "Detalle del Presupuesto"

    presupuesto_id =  fields.Many2one(
        comodel_name='presupuesto',
        string="Presupuesto"
    )
    name = fields.Many2one(
        comodel_name='recurso.cinematografico',
        string="Recurso"
    )
    producto_id = fields.Many2one(
        comodel_name='product.product',
        string="Producto"
    )
    descripcion = fields.Char(related='name.descripcion',string="Descripción")
    precio = fields.Float(string="Precio",digits='Product Price')
    contacto_id = fields.Many2one(
        related='name.contacto_id',
        comodel_name='res.partner',
        string="Contacto"
    )
    imagen = fields.Binary(related='name.imagen',string="Imagen")
    cantidad = fields.Float(string="Cantidad",default=1.0,digits=(16,4))
    importe = fields.Monetary(string="Importe",readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='presupuesto_id.currency_id',
        string="Moneda",
        readonly=True
    )
    sequence = fields.Integer()

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.precio = self.name.precio
        else:
            self.precio = False

    @api.onchange('cantidad','precio')
    def _onchange_importe(self):
        self.importe = self.cantidad * self.precio

class ProductExtended(models.Model):
    _inherit = "product.product"

    def name_get(self):
        result = []
        for product in self:
            name = '[%s] %s' % (product.barcode,product.name)
            result.append((product.id,name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += ['|', ('name', operator, name), ('barcode', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)