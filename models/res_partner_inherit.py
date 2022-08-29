# -*- coding:utf-8 -*-

from odoo import fields, models, api

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    customer_rank = fields.Integer(default=0, copy=False)

    def get_items(self):
        self.ensure_one()
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Productos',
            'view_mode' : 'tree,form',
            'res_model' : 'presupuesto',
            #'domain' : '[('', '', '')]'
            'context' : "{'create': False}"
        }