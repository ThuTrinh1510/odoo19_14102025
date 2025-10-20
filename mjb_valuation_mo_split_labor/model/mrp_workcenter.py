# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval
from odoo import models, fields, api
from odoo.http import request

class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    @api.depends('employee_id.hourly_cost')
    def _compute_employee_cost(self):
        super(MrpWorkcenterProductivity,self)._compute_employee_cost()
        for time in self:
            if not time.employee_id.x_use_employee_cost_in_manufacturing:
                time.employee_cost = time.workcenter_id.employee_costs_hour if time.workcenter_id.employee_costs_hour else time.employee_id.hourly_cost