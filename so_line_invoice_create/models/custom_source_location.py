# -*- coding: utf-8 -*-

from odoo import models, fields


class SourceLocation(models.Model):
    _name = 'custom.source.location'
    _description = 'Custom Source Location'

    name = fields.Char(
        string='Name',
        required=True,
    )
    stock_location_id = fields.Many2one(
        'stock.location',
        'Source Location',
        required=True,
    )
