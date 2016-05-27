# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010
#    OpenERP Italian Community (<http://www.openerp-italia.org>)
#    Servabit srl
#    Agile Business Group sagl
#    Domsense srl
#    Albatos srl
#
#    Copyright (C) 2011-2012
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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
    'name': 'Customization partner B2Pharma',
    'version': '0.2',
    'depends': ['base_vat','account_chart','base_iban'],
    'author': 'Isa s.r.l.',
    'description': """
Piano dei conti italiano b2pharma.
================================================

B2pharma accounting chart and localization.
    """,
    'license': 'AGPL-3',
    'category': 'Localization/Account Charts',
    'website': 'http://www.isa.it/',
    'depends': ['base',
                'l10n_it_base',
                'l10n_it',
                ],    
    'data': ['views/res_partner.xml',],
    'installable': True,
    'auto_install': False,
}
