# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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

from openerp.osv import osv, fields

# definizione di tre tabelle gerarchiche come i tag dei partner:
# settore, attivita, categoria
#
# per ogni tabella creo una tabella di legame con i partner (come fra prodotti
#  e fornitori, ecc.) in modo da avere un ulteriore livello di dati (form aggiungi
#  riga ed eventuali altre informazioni)


class res_partner_settore(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        """Return the sectors' display name, including their direct
           parent by default.

        :param dict context: the ``partner_settoredisplay`` key can be
                             used to select the short version of the
                             sector name (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if context is None:
            context = {}
        if context.get('partner_settore_display') == 'short':
            return super(res_partner_settore, self).name_get(cr, uid, ids, context=context)
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _description = 'Settori clienti'
    _name = 'res.partner.settore'
    _columns = {
        'name': fields.char('Sector Name', required=True, size=64, translate=True, select=True),
        'parent_id': fields.many2one('res.partner.settore', 'Parent Sector', select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'child_ids': fields.one2many('res.partner.settore', 'parent_id', 'Child Sectors'),
        'active': fields.boolean('Active', help="The active field allows you to hide the sector without removing it."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
    }
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active': 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'


class res_partner_settoreinfo(osv.osv):
    _name = "res.partner.settoreinfo"
    _description = "Information about a customer sector"

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer','=',True)], ondelete='cascade', help="Customer in this sector"),
        'nota': fields.char('Note', size=64, help="Eventuali note."),
        'name': fields.many2one('res.partner.settore', 'Sector', required=True, ondelete='cascade'),
    }


class res_partner_attivita(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        """Return the activities' display name, including their direct
           parent by default.

        :param dict context: the ``partner_attivita_display`` key can be
                             used to select the short version of the
                             activity name (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if context is None:
            context = {}
        if context.get('partner_attivita_display') == 'short':
            return super(res_partner_attivita, self).name_get(cr, uid, ids, context=context)
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _description = 'Attivita clienti'
    _name = 'res.partner.attivita'
    _columns = {
        'name': fields.char('Activity Name', required=True, size=64, translate=True),
        'parent_id': fields.many2one('res.partner.attivita', 'Parent Activity', select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'child_ids': fields.one2many('res.partner.attivita', 'parent_id', 'Child Activities'),
        'active': fields.boolean('Active', help="The active field allows you to hide the activity without removing it."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
    }
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You can not create recursive activities.', ['parent_id'])
    ]
    _defaults = {
        'active': 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'


class res_partner_attivitainfo(osv.osv):
    _name = "res.partner.attivitainfo"
    _description = "Information about a customer activity"

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer','=',True)], ondelete='cascade', help="Customer in this activity"),
        'nota': fields.char('Note', size=64, help="Eventuali note."),
        'name': fields.many2one('res.partner.attivita', 'Activity', required=True, ondelete='cascade'),
    }


class res_partner_categoria(osv.osv):

    def name_get(self, cr, uid, ids, context=None):
        """Return the categories' display name, including their direct
           parent by default.

        :param dict context: the ``partner_categoria_display`` key can be
                             used to select the short version of the
                             category name (without the direct parent),
                             when set to ``'short'``. The default is
                             the long version."""
        if context is None:
            context = {}
        if context.get('partner_categoria_display') == 'short':
            return super(res_partner_categoria, self).name_get(cr, uid, ids, context=context)
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _description = 'Categorie clienti'
    _name = 'res.partner.categoria'
    _columns = {
        'name': fields.char('Category Name', required=True, size=64, translate=True),
        'parent_id': fields.many2one('res.partner.categoria', 'Parent Category', select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'child_ids': fields.one2many('res.partner.categoria', 'parent_id', 'Child Categories'),
        'active': fields.boolean('Active', help="The active field allows you to hide the category without removing it."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
    }
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active': 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'


class res_partner_categoinfo(osv.osv):
    _name = "res.partner.categoinfo"
    _description = "Information about a customer category"

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer','=',True)], ondelete='cascade', help="Customer in this sector"),
        'nota': fields.char('Note', size=64, help="Eventuali note."),
        'name': fields.many2one('res.partner.categoria', 'Category', required=True, ondelete='cascade'),
    }


class res_partner(osv.osv):

    _inherit = "res.partner"

    _columns = {
        'categoria_ids': fields.one2many('res.partner.categoinfo', 'partner_id', 'Categoria'),
        'attivita_ids': fields.one2many('res.partner.attivitainfo', 'partner_id', 'Attivita'),
        'settore_ids': fields.one2many('res.partner.settoreinfo', 'partner_id', 'Settore'),
        }
