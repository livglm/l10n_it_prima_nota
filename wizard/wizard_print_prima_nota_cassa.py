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
import time
from openerp.osv import fields, orm
from openerp import api,_
class account_report_prima_nota(orm.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.report.prima_nota'
    _description = "Print Prima Nota Cassa"


    def _get_all_journal(self, cr, uid, context=None):
        return self.pool.get('account.journal').search(cr, uid , [('type','in',['cash','bank'])] )

    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        data = self.pre_print_report(cr, uid, ids, data, context=context)

        data['form'].update(self.read(cr, uid, ids, ['landscape',  'initial_balance', 'amount_currency', 'sortby'])[0])
        #data['form'].update(self.read(cr, uid, ids, [ 'initial_balance'])[0])

        if not data['form']['fiscalyear_id']:# GTK client problem onchange does not consider in save record
            data['form'].update({'initial_balance': False})

        #data.update({'time': time})
        #data.update({'lines': self.lines})

        print data
        #return { 'type': 'ir.actions.report.xml', 'report_name': 'account.print.prima_nota_cassa', 'datas': data}
        return { 'type': 'ir.actions.report.xml', 'report_name': 'l10n_it_prima_nota.prima_nota', 'datas': data}



    _columns = {
        'initial_balance': fields.boolean('Include initial balances', help='It adds initial balance row on report which display previous sum amount of debit/credit/balance'),
    }
    _defaults = {
        'journal_ids': _get_all_journal,
    }


    # @api.multi
    # def __init__(self):
    #     if self.context is None:
    #         context = {}
    #     super(account_report_prima_nota, self).__init__()
    #     self.query = ""
    #     self.tot_currency = 0.0
    #     self.period_sql = ""
    #     self.sold_accounts = {}
    #     self.sortby = 'sort_date'
    #     self.localcontext.update( {
    #          'time': time,
    #          'lines': self.lines,
    #          'sum_debit_account': self._sum_debit_account,
    #          'sum_credit_account': self._sum_credit_account,
    #          'sum_balance_account': self._sum_balance_account,
    #          'sum_currency_amount_account': self._sum_currency_amount_account,
    #          'get_fiscalyear': self._get_fiscalyear,
    #          'get_journal': self._get_journal,
    #          'get_account': self._get_account,
    #          'get_start_period': self.get_start_period,
    #          'get_end_period': self.get_end_period,
    #          'get_filter': self._get_filter,
    #          'get_sortby': self._get_sortby,
    #          'get_start_date':self._get_start_date,
    #          'get_end_date':self._get_end_date,
    #          'get_target_move': self._get_target_move,
    #      })
    #     self.context = context




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
