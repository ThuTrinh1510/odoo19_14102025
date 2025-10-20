from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_split_labor_cost_mo_entry(self):
        for rec in self:
            for move in rec.stock_move_ids:
                
                rec.splitLaborCostEntry(move)

    def splitLaborCostEntry(self, move):
        # get related stock move
        stockMove = move
        if not stockMove:
            print("No stock move")
            return False

        # get related production order for finished goods
        productionOrder = stockMove.production_id
        if not productionOrder:
            print("No production order")
            return False

        # get related product
        product = productionOrder.product_id
        print('product', product)
        if not product:
            print("No product")
            return False

        LABOUR_ACCOUNT_ID = product.categ_id.labour_valuation_account_id.id
        OVERHEAD_ACCOUNT_ID = product.categ_id.overhead_valuation_account_id.id
        VALUATION_ACCOUNT_ID = product.categ_id.property_stock_valuation_account_id.id
        MATERIAL_ACCOUNT_ID = stockMove.production_id.production_location_id.valuation_out_account_id.id
        if not MATERIAL_ACCOUNT_ID:
            MATERIAL_ACCOUNT_ID = product.categ_id.property_stock_account_production_cost_id.id
        if not LABOUR_ACCOUNT_ID or not OVERHEAD_ACCOUNT_ID or not VALcunUATION_ACCOUNT_ID or not MATERIAL_ACCOUNT_ID:
            print("Missing accounts")
            return False

        # Find the debit line
        print("Can work")
        debitLine = False
        hasLabour = False
        for l in self.line_ids:
            if l.account_id.id == VALUATION_ACCOUNT_ID:
                debitLine = l
            if l.account_id.id == LABOUR_ACCOUNT_ID:
                hasLabour = True

        # only continue if not already done
        if hasLabour:
            print('has labour entries, skip')
            return False

        # getWorkorder cost
        workOrders = productionOrder.workorder_ids
        toCreate = []
        labourValue = 0.0
        overheadValue = 0.0
        index = 0
        productValue = debitLine.debit

        for wo in workOrders:
            for employee in wo.time_ids:
                emp_cost = (employee.duration or 0.0) * (wo.workcenter_id.employee_costs_hour or 0.0) / 60
                if emp_cost > 0.0:
                    labourValue += round(emp_cost, 2)
                    toCreate.append((0, 0, {
                        "credit": round(emp_cost, 2),
                        "debit": 0.0,
                        "account_id": LABOUR_ACCOUNT_ID,
                        "name": f"{productionOrder.name} - {wo.name} - {employee.employee_id.name}",
                        "currency_id": self.currency_id.id
                    }))
                    index += 1

            wc_cost = (wo.duration or 0.0) * (wo.workcenter_id.costs_hour or 0.0) / 60
            if wc_cost > 0.0:
                overheadValue += round(wc_cost, 2)
                toCreate.append((0, 0, {
                    "credit": round(wc_cost, 2),
                    "debit": 0.0,
                    "account_id": OVERHEAD_ACCOUNT_ID,
                    "name": f"{productionOrder.name} - {wo.name} - Overhead",
                    "currency_id": self.currency_id.id
                }))

        if index == 0:
            print("No WO time for cost, skip")
            return False

        # Material cost
        material_cost = round((productValue - labourValue - overheadValue), 2)
        if material_cost > 0:
            toCreate.append((0, 0, {
                "credit": material_cost,
                "debit": 0.0,
                "account_id": MATERIAL_ACCOUNT_ID,
                "name": debitLine.name,
                "currency_id": self.currency_id.id
            }))
        elif material_cost < 0:
            toCreate.append((0, 0, {
                "credit": 0.0,
                "debit": material_cost * -1,
                "account_id": MATERIAL_ACCOUNT_ID,
                "name": debitLine.name,
                "currency_id": self.currency_id.id
            }))

        # Product Value
        if productValue > 0:
            toCreate.append((0, 0, {
                "credit": 0.0,
                "debit": productValue,
                "account_id": VALUATION_ACCOUNT_ID,
                "name": debitLine.name,
                "currency_id": self.currency_id.id
            }))

        if self.state == 'posted':
            self.sudo().button_draft()
            # self.env.cr.commit()

        self.line_ids.sudo().unlink()
        self.sudo().write({
            'line_ids': toCreate
        })
        # self.env.cr.commit()
        self.sudo().action_post()
        return True