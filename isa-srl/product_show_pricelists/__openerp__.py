# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 ISA s.r.l. (<http://www.isa.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product Show Pricelist',
    'version': '0.1',
    'category': '',
    'description': """
Questo modulo permette di visualizzare, sulle viste dei prodotti e dei template di prodotti, i listini associati, con tanto di calcolo del prezzo.
       """,
    'author': 'ISA srl',
    'depends': [
                'product',
                'account',
                'product_variant_grid',
                'product_pricelist_customization',
                ],
    'data': ['views/product_view.xml',],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
