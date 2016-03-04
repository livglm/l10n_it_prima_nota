# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import datetime
from openerp import api,_, models,fields



class account_report_prima_nota(models.TransientModel):
    _inherit = "account.common.account.report"
    #_inherit = "account.move.line"
    _name = 'account.report.prima_nota'
    _description = "Print Prima Nota Cassa"

    def _get_all_journal(self, cr, uid, context=None):
        return self.pool.get('account.journal').search(cr, uid , [('type','in',['cash','bank'])] )

    def lines(self, main_account):
        """ Return all the account_move_line of account with their account code counterparts """
        account_ids = self.env['account.move.line'].get_children_accounts(main_account)

        move_state = ['draft','posted']
        if self.target_move == 'posted':
            move_state = ['posted', '']

        # Then select all account_move_line of this account
        if self.sortby == 'sort_journal_partner':
            sql_sort='j.code, p.name, l.move_id'
        else:
            sql_sort='l.date, l.move_id'
        sql = """
            SELECT
                l.id AS lid,
                l.date AS ldate,
                j.code AS lcode,
                j.name AS jname,
                l.currency_id,
                l.amount_currency,
                l.ref AS lref,
                l.name AS lname,
                COALESCE(l.debit,0) AS debit,
                COALESCE(l.credit,0) AS credit,
                l.period_id AS lperiod_id,
                l.partner_id AS lpartner_id,
                m.name AS move_name,
                m.id AS mmove_id,
                per.code as period_code,
                c.symbol AS currency_code,
                i.id AS invoice_id,
                i.type AS invoice_type,
                i.number AS invoice_number,
                p.name AS partner_name
            FROM account_move_line l
            JOIN account_move m on (l.move_id=m.id)
            LEFT JOIN res_currency c on (l.currency_id=c.id)
            LEFT JOIN res_partner p on (l.partner_id=p.id)
            LEFT JOIN account_invoice i on (m.id =i.move_id)
            LEFT JOIN account_period per on (per.id=l.period_id)
            JOIN account_journal j on (l.journal_id=j.id)
            WHERE %s
                AND m.state IN %s
                AND l.account_id in %%s
            ORDER by %s
        """ %(self.query, tuple(move_state), sql_sort)
        self.cr.execute(sql, (tuple(account_ids),))
        res = self.cr.dictfetchall()
        for l in res:
            l['move'] = l['move_name'] != '/' and l['move_name'] or ('*'+str(l['mmove_id']))
            l['partner'] = l['partner_name'] or ''
            # Modification of amount Currency
            if l['credit'] > 0:
                if l['amount_currency'] != None:
                    l['amount_currency'] = abs(l['amount_currency']) * -1
            if l['amount_currency'] != None:
                self.tot_currency = self.tot_currency + l['amount_currency']
        print res
        return res




    @api.multi
    def _print_report(self,data=None):
        if self._context is None:
            self._context = {}
        #
        # self.query = ""
        # self.tot_currency = 0.0
        # self.period_sql = ""
        # self.sold_accounts = {}
        # self.sortby = 'sort_date'
        #
        id = self.lines
        print id
        #data = self.pre_print_report()

        #data['form'].update(self.read(['landscape',  'initial_balance', 'amount_currency', 'sortby'])[0])
        #data['form'].update(self.read(cr, uid, ids, [ 'initial_balance'])[0])

        #if not data['form']['fiscalyear_id']:# GTK client problem onchange does not consider in save record
        #    data['form'].update({'initial_balance': False})

        #data.update({'time': time})
        #data.update({'lines': self.lines})

        datas = {'ids' : [id],
                 'model':'account.move.line',
                 'form': self.read()
        }

        print datas
        #return { 'type': 'ir.actions.report.xml', 'report_name': 'account.print.prima_nota_cassa', 'datas': data}
        return { 'type': 'ir.actions.report.xml','report_name': 'ln10_it_prima_nota.prima_nota', 'datas': datas}

        #return self.pool.get('account_report_prima_nota').get_action(cr, uid, [], 'ln10_it_prima_nota.prima_nota', data=data)


    initial_balance = fields.Boolean('Include initial balances', help='It adds initial balance row on report which display previous sum amount of debit/credit/balance')

    #
    #  _defaults = {
    #     'journal_ids': _get_all_journal,
    # }




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
