# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.tools import date_utils


class AccountMove(models.Model):
    _inherit = "account.account"

    x_show_in_unrealized_gl_rp = fields.Boolean(string='Show in Unrealized currency gain/loss report', default=False, store=True)