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
        print main_account
        account_ids = self.env['account.move.line'].get_children_accounts(main_account)

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

        datas = {'ids' : [],
                 'model':'account.move.line',
                 'form': self.read()
        }

        print datas
        #return { 'type': 'ir.actions.report.xml', 'report_name': 'account.print.prima_nota_cassa', 'datas': data}
        #return { 'type': 'ir.actions.report.xml','report_name': 'ln10_it_prima_nota.prima_nota', 'datas': datas}

        #return self.pool.get('account_report_prima_nota').get_action(cr, uid, [], 'ln10_it_prima_nota.prima_nota', data=data)


    initial_balance = fields.Boolean('Include initial balances', help='It adds initial balance row on report which display previous sum amount of debit/credit/balance')

    #
    #  _defaults = {
    #     'journal_ids': _get_all_journal,
    # }




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
