from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    labour_valuation_account_id = fields.Many2one('account.account', string="Labor Valuation Account")
    overhead_valuation_account_id = fields.Many2one('account.account', string="Overhead Valuation Account")