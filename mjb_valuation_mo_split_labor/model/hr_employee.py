# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    x_use_employee_cost_in_manufacturing = fields.Boolean(string="Use employee cost in manufacturing",default=False)

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    x_use_employee_cost_in_manufacturing = fields.Boolean(related="employee_id.x_use_employee_cost_in_manufacturing",string="Use employee cost in manufacturing",readonly=True)