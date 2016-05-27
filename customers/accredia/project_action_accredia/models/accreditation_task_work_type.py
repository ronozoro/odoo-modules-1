# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2013 ISA s.r.l. (<http://www.isa.it>).
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

from openerp import fields, models


class AccreditationTaskWorkType(models.Model):

    _inherit = 'accreditation.task.work.type'

    doclite_action_type = fields.Selection([('mail', 'Invio Mail'),
                                            ('document', 'Generazione Documento'),
                                            ('folder', 'Generazione Folder Virtuale'),
                                            ('archive', 'Archivia Documento'),
                                            ],
                                           'Tipo Azione DocLite', select=True)
    doclite_action_model = fields.Many2one('doclite.document.model', 'Modello Documento DocLite')
    doclite_action_category = fields.Many2one('doclite.document.category', 'Categoria Documento DocLite')
