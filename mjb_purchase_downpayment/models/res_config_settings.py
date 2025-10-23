# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.addons.account.models.company import PEPPOL_LIST


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    purchase_downpayment_account_id = fields.Many2one(
        'account.account',
        string="Purchase Downpayent Account",
        related='company_id.purchase_downpayment_account_id',
        default_model='res.company',
        readonly=False,
        check_company=True,
    )