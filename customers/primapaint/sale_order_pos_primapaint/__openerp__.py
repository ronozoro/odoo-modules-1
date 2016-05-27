# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2015 ISA srl (<http://www.isa.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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

{
    'name': 'Sale Order Pos Primapaint',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """

Questo modulo introduce il tasto stampa scontrino sugli ordini di vendita.

================================================================================    
    
""",
    'author': 'ISA srl',
    'depends': [
                'product',
                'sale',
                'sale_stock',
                'stock',                
                ],
    'data': [
             'views/sale_order_view.xml',  
             'wizard/wizard_sale_print_bill_view.xml', 
             ],
    'installable': True,
    'auto_install': False,
    'certificate': '',
}
