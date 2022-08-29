# -*- coding:utf-8 -*-

from odoo import fields, models, api

class RecursoCinematografico(models.Model):
    _name = "recurso.cinematografico"
    _description = "Recurso Cinematografico"

    _sql_constraints = [
        ('name_unique', 'unique (name)', "El nombre del registo ya existe!"),
    ]

    name = fields.Char(string="Recurso")
    descripcion = fields.Char(string="Descripción")
    precio = fields.Float(string="Precio")
    contacto_id = fields.Many2one(
        comodel_name='res.partner',
        domain="[('is_company', '=', False)]",
        string="Contacto"
    )
    imagen = fields.Binary(string="Imagen")