from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

import logging


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    bar_qty = fields.Float(string='Bar Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True)

    no_change_bar_qty = False

    @api.onchange('bar_qty')
    def onchange_bar_qty(self):

        if self.no_change_bar_qty:
            self.no_change_bar_qty = False
            return

        if self.bar_qty != 0 and self.product_id.weight != 0:
            self.product_qty = self.bar_qty * self.product_id.weight

    @api.onchange('product_qty')
    def onchange_product_quantity(self):

        self.no_change_bar_qty = True

        if self.product_qty == 0 or self.product_id.weight == 0:
            self.bar_qty = 0
        else:
            self.bar_qty = self.product_qty / self.product_id.weight