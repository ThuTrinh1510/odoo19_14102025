# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare
import logging
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare, float_is_zero, float_round
from itertools import groupby
_logger = logging.getLogger(__name__)

class Company(models.Model):
    _inherit = 'res.company'
    
    
    purchase_downpayment_account_id = fields.Many2one(
        'account.account', string="Purchase Downpayment Account")