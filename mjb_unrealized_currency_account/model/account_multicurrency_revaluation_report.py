# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import float_is_zero, SQL
from odoo.exceptions import UserError

from itertools import chain


class MulticurrencyRevaluationReportCustomHandler(models.AbstractModel):
    _inherit = 'account.multicurrency.revaluation.report.handler'

    def _multi_currency_revaluation_get_custom_lines(self, options, line_code, current_groupby, next_groupby, offset=0, limit=None):
        def build_result_dict(report, query_res):
            return {
                'balance_currency': query_res['balance_currency'] if len(query_res['currency_id']) == 1 else None,
                'currency_id': query_res['currency_id'][0] if len(query_res['currency_id']) == 1 else None,
                'balance_operation': query_res['balance_operation'],
                'balance_current': query_res['balance_current'],
                'adjustment': query_res['adjustment'],
                'has_sublines': True,
            }

        report = self.env['account.report'].browse(options['report_id'])
        report._check_groupby_fields((next_groupby.split(',') if next_groupby else []) + ([current_groupby] if current_groupby else []))

        # No need to run any SQL if we're computing the main line: it does not display any total
        if not current_groupby:
            return {
                'balance_currency': None,
                'currency_id': None,
                'balance_operation': None,
                'balance_current': None,
                'adjustment': None,
                'has_sublines': True,
            }

        query = "(VALUES {})".format(', '.join("(%s, %s)" for rate in options['currency_rates']))
        params = list(chain.from_iterable((cur['currency_id'], cur['rate']) for cur in options['currency_rates'].values()))
        custom_currency_table_query = SQL(query, *params)
        date_to = options['date']['date_to']
        select_part_not_an_exchange_move_id = SQL(
            """
            NOT EXISTS (
                SELECT 1
                  FROM account_partial_reconcile part_exch
                 WHERE part_exch.exchange_move_id = account_move_line.move_id
                   AND part_exch.max_date <= %s
            )
            """,
            date_to
        )

        query = report._get_report_query(options, 'strict_range')
        groupby_field_sql = self.env['account.move.line']._field_to_sql("account_move_line", current_groupby, query)
        tail_query = report._get_engine_query_tail(offset, limit)
        full_query = SQL(
            """
            WITH custom_currency_table(currency_id, rate) AS (%(custom_currency_table_query)s)

            -- Final select that gets the following lines:
            -- (where there is a change in the rates of currency between the creation of the move and the full payments)
            -- - Moves that don't have a payment yet at a certain date
            -- - Moves that have a partial but are not fully paid at a certain date
            SELECT
                   subquery.grouping_key,
                   ARRAY_AGG(DISTINCT(subquery.currency_id)) AS currency_id,
                   SUM(subquery.balance_currency) AS balance_currency,
                   SUM(subquery.balance_operation) AS balance_operation,
                   SUM(subquery.balance_current) AS balance_current,
                   SUM(subquery.adjustment) AS adjustment
              FROM (
                -- Get moves that have at least one partial at a certain date and are not fully paid at that date
                SELECT
                       %(groupby_field_sql)s AS grouping_key,
                       ROUND(account_move_line.balance - SUM(ara.amount_debit) + SUM(ara.amount_credit), aml_comp_currency.decimal_places) AS balance_operation,
                       ROUND(account_move_line.amount_currency - SUM(ara.amount_debit_currency) + SUM(ara.amount_credit_currency), aml_currency.decimal_places) AS balance_currency,
                       ROUND(account_move_line.amount_currency - SUM(ara.amount_debit_currency) + SUM(ara.amount_credit_currency), aml_currency.decimal_places) / custom_currency_table.rate AS balance_current,
                       (
                          -- adjustment is computed as: balance_current - balance_operation
                          ROUND( account_move_line.amount_currency - SUM(ara.amount_debit_currency) + SUM(ara.amount_credit_currency), aml_currency.decimal_places) / custom_currency_table.rate
                          - ROUND(account_move_line.balance - SUM(ara.amount_debit) + SUM(ara.amount_credit), aml_comp_currency.decimal_places)
                       ) AS adjustment,
                       account_move_line.currency_id AS currency_id,
                       account_move_line.id AS aml_id
                  FROM %(table_references)s,
                       account_account AS account,
                       res_currency AS aml_currency,
                       res_currency AS aml_comp_currency,
                       custom_currency_table,

                       -- Get for each move line the amount residual and amount_residual currency
                       -- both for matched "debit" and matched "credit" the same way as account.move.line
                       -- '_compute_amount_residual()' method does
                       -- (using LATERAL greatly reduce the number of lines for which we have to compute it)
                       LATERAL (
                               -- Get sum of matched "debit" amount and amount in currency for related move line at date
                               SELECT COALESCE(SUM(part.amount), 0.0) AS amount_debit,
                                      ROUND(
                                          SUM(part.debit_amount_currency),
                                          curr.decimal_places
                                      ) AS amount_debit_currency,
                                      0.0 AS amount_credit,
                                      0.0 AS amount_credit_currency,
                                      account_move_line.currency_id AS currency_id,
                                      account_move_line.id AS aml_id
                                 FROM account_partial_reconcile part
                                 JOIN res_currency curr ON curr.id = part.debit_currency_id
                                WHERE account_move_line.id = part.debit_move_id
                                  AND part.max_date <= %(date_to)s
                             GROUP BY aml_id,
                                      curr.decimal_places
                           UNION
                               -- Get sum of matched "credit" amount and amount in currency for related move line at date
                               SELECT 0.0 AS amount_debit,
                                      0.0 AS amount_debit_currency,
                                      COALESCE(SUM(part.amount), 0.0) AS amount_credit,
                                      ROUND(
                                          SUM(part.credit_amount_currency),
                                          curr.decimal_places
                                      ) AS amount_credit_currency,
                                      account_move_line.currency_id AS currency_id,
                                      account_move_line.id AS aml_id
                                 FROM account_partial_reconcile part
                                 JOIN res_currency curr ON curr.id = part.credit_currency_id
                                WHERE account_move_line.id = part.credit_move_id
                                  AND part.max_date <= %(date_to)s
                             GROUP BY aml_id,
                                      curr.decimal_places
                            ) AS ara
                 WHERE %(search_condition)s
                   AND account_move_line.account_id = account.id
                   AND account_move_line.currency_id = aml_currency.id
                   AND account_move_line.company_currency_id = aml_comp_currency.id
                   AND account_move_line.currency_id = custom_currency_table.currency_id
                   AND account.x_show_in_unrealized_gl_rp IS True
                   -- AND account.account_type NOT IN ('income', 'income_other', 'expense', 'expense_depreciation', 'expense_direct_cost', 'off_balance')
                   AND (
                        account.currency_id != account_move_line.company_currency_id
                        OR (
                            (account.account_type IN ('asset_receivable', 'liability_payable') OR account.currency_id IS NULL)
                            AND (account_move_line.currency_id != account_move_line.company_currency_id)
                        )
                   )
                   AND %(exist_condition)s (
                        SELECT 1
                          FROM account_account_exclude_res_currency_provision
                         WHERE account_account_id = account_move_line.account_id
                           AND res_currency_id = account_move_line.currency_id
                   )
                   AND (%(select_part_not_an_exchange_move_id)s)
              GROUP BY account_move_line.id, grouping_key, aml_comp_currency.decimal_places,  aml_currency.decimal_places, custom_currency_table.rate
                HAVING ROUND(account_move_line.balance - SUM(ara.amount_debit) + SUM(ara.amount_credit), aml_comp_currency.decimal_places) != 0
                    OR ROUND(account_move_line.amount_currency - SUM(ara.amount_debit_currency) + SUM(ara.amount_credit_currency), aml_currency.decimal_places) != 0.0

                UNION
                -- Moves that don't have a payment yet at a certain date
                SELECT
                       %(groupby_field_sql)s AS grouping_key,
                       account_move_line.balance AS balance_operation,
                       account_move_line.amount_currency AS balance_currency,
                       account_move_line.amount_currency / custom_currency_table.rate AS balance_current,
                       account_move_line.amount_currency / custom_currency_table.rate - account_move_line.balance AS adjustment,
                       account_move_line.currency_id AS currency_id,
                       account_move_line.id AS aml_id
                  FROM %(table_references)s
                  JOIN account_account account ON account_move_line.account_id = account.id
                  JOIN custom_currency_table ON custom_currency_table.currency_id = account_move_line.currency_id
                 WHERE %(search_condition)s
                   -- AND account.account_type NOT IN ('income', 'income_other', 'expense', 'expense_depreciation', 'expense_direct_cost', 'off_balance')
                   AND account.x_show_in_unrealized_gl_rp IS True
                   AND (
                        account.currency_id != account_move_line.company_currency_id
                        OR (
                            (account.account_type IN ('asset_receivable', 'liability_payable') OR account.currency_id IS NULL)
                            AND (account_move_line.currency_id != account_move_line.company_currency_id)
                        )
                   )
                   AND %(exist_condition)s (
                        SELECT 1
                          FROM account_account_exclude_res_currency_provision
                         WHERE account_account_id = account_id
                           AND res_currency_id = account_move_line.currency_id
                   )
                   AND (%(select_part_not_an_exchange_move_id)s)
                   AND NOT EXISTS (
                        SELECT 1 FROM account_partial_reconcile part
                        WHERE (part.debit_move_id = account_move_line.id OR part.credit_move_id = account_move_line.id)
                          AND part.max_date <= %(date_to)s
                   )
                   AND (account_move_line.balance != 0.0 OR account_move_line.amount_currency != 0.0)

            ) subquery

            GROUP BY grouping_key
            ORDER BY grouping_key
            %(tail_query)s
            """,
            groupby_field_sql=groupby_field_sql,
            custom_currency_table_query=custom_currency_table_query,
            exist_condition=SQL('NOT EXISTS') if line_code == 'to_adjust' else SQL('EXISTS'),
            table_references=query.from_clause,
            date_to=date_to,
            tail_query=tail_query,
            search_condition=query.where_clause,
            select_part_not_an_exchange_move_id=select_part_not_an_exchange_move_id,
        )
        
        self.env.cr.execute(full_query)
        query_res_lines = self.env.cr.dictfetchall()

        rslt = []
        for query_res in query_res_lines:
            grouping_key = query_res['grouping_key']
            rslt.append((grouping_key, build_result_dict(report, query_res)))
        return rslt


