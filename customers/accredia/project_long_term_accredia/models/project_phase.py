# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from openerp.tools.translate import _
from openerp.osv import fields, osv


class project_phase(osv.osv):
    _name = "project.phase"
    _description = "Project Phase"

    def _check_recursion(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        data_phase = self.browse(cr, uid, ids[0], context=context)
        prev_ids = data_phase.previous_phase_ids
        next_ids = data_phase.next_phase_ids
        # it should neither be in prev_ids nor in next_ids
        if (data_phase in prev_ids) or (data_phase in next_ids):
            return False
        ids = [id for id in prev_ids if id in next_ids]
        # both prev_ids and next_ids must be unique
        if ids:
            return False
        # unrelated project
        prev_ids = [rec.id for rec in prev_ids]
        next_ids = [rec.id for rec in next_ids]
        # iter prev_ids
        while prev_ids:
            cr.execute('SELECT distinct prv_phase_id FROM project_phase_rel WHERE next_phase_id IN %s', (tuple(prev_ids),))
            prv_phase_ids = filter(None, map(lambda x: x[0], cr.fetchall()))
            if data_phase.id in prv_phase_ids:
                return False
            ids = [id for id in prv_phase_ids if id in next_ids]
            if ids:
                return False
            prev_ids = prv_phase_ids
        # iter next_ids
        while next_ids:
            cr.execute('SELECT distinct next_phase_id FROM project_phase_rel WHERE prv_phase_id IN %s', (tuple(next_ids),))
            next_phase_ids = filter(None, map(lambda x: x[0], cr.fetchall()))
            if data_phase.id in next_phase_ids:
                return False
            ids = [id for id in next_phase_ids if id in prev_ids]
            if ids:
                return False
            next_ids = next_phase_ids
        return True

    def _check_dates(self, cr, uid, ids, context=None):
        for phase in self.read(cr, uid, ids, ['date_start', 'date_end'], context=context):
            if phase['date_start'] and phase['date_end'] and phase['date_start'] > phase['date_end']:
                return False
        return True

    def _compute_progress(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for phase in self.browse(cr, uid, ids, context=context):
            if phase.state == 'done':
                res[phase.id] = 100.0
                continue
            elif phase.state == "cancelled":
                res[phase.id] = 0.0
                continue
            elif not phase.task_ids:
                res[phase.id] = 0.0
                continue

            tot = done = 0.0
            for task in phase.task_ids:
                tot += task.total_hours
                done += min(task.effective_hours, task.total_hours)

            if not tot:
                res[phase.id] = 0.0
            else:
                res[phase.id] = round(100.0 * done / tot, 2)
        return res

    def _compute_dates(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        if not isinstance(fields, list):
            fields = [fields]
        for phase in self.browse(cr, uid, ids, context=context):
            t_date_start = None
            t_date_end = None
            t_duration = 0.0
            for allocation in phase.user_ids:
                if allocation.date_start and (not phase.date_start or allocation.date_start < phase.date_start):
                    t_date_start = allocation.date_start
                if allocation.date_end and (not phase.date_end or allocation.date_end < phase.date_end):
                    t_date_end = allocation.date_end
                if allocation.num_days:
                    t_duration += allocation.num_days


            phase_data = {}
            res[phase.id] = phase_data
            for field in fields:
                if field == 'date_start':
                    phase_data[field] = t_date_start
                elif field == 'date_end':
                    phase_data[field] = t_date_end
                elif field == 'duration':
                    phase_data[field] = t_duration
        return res

    def _get_product_uom(self, cr, uid, context=None):
        uom = None
        try:
            t_uom = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'product', 'product_uom_day')
            uom = t_uom[1]
        except ValueError:
            pass
        return uom

    _columns = {
        'name': fields.char("Name", size=64, required=True),
        'date_start': fields.function(_compute_dates, string='Start Date', type="date", multi='dates', store=True, readonly=True),
        'date_end': fields.function(_compute_dates, string='End Date', type="date", multi='dates', store=True, readonly=True),
        'duration': fields.function(_compute_dates, string='Totale GG uomo', type="float", multi='dates', store=True, readonly=True),
        'constraint_date_start': fields.date('Minimum Start Date', help='force the phase to start after this date',
                                             states={'confirmed':[('readonly',True)], 'done':[('readonly',True)], 'cancelled':[('readonly',True)]}),
        'constraint_date_end': fields.date('Deadline', help='force the phase to finish before this date',
                                           states={'confirmed':[('readonly',True)], 'done':[('readonly',True)], 'cancelled':[('readonly',True)]}),
        'project_id': fields.many2one('project.project', 'Project', required=True, select=True,
                                      states={'confirmed':[('readonly',True)], 'done':[('readonly',True)], 'cancelled':[('readonly',True)]}),
        'next_phase_ids': fields.many2many('project.phase', 'project_phase_rel', 'prv_phase_id', 'next_phase_id', 'Next Phases',
                                           states={'cancelled':[('readonly',True)]}),
        'previous_phase_ids': fields.many2many('project.phase', 'project_phase_rel', 'next_phase_id', 'prv_phase_id', 'Previous Phases',
                                               states={'cancelled':[('readonly',True)]}),
        'sequence': fields.integer('Sequence', select=True, help="Gives the sequence order when displaying a list of phases."),
        'product_uom': fields.many2one('product.uom', 'Duration Unit of Measure', required=True, help="Unit of Measure (Unit of Measure) is the unit of measurement for Duration",
                                       states={'confirmed':[('readonly',True)], 'done':[('readonly',True)], 'cancelled':[('readonly',True)]}),
        'task_ids': fields.one2many('project.task', 'phase_id', "Project Tasks",
                                    states={'confirmed':[('readonly',True)], 'done':[('readonly',True)], 'cancelled':[('readonly',True)]}),
        'user_force_ids': fields.many2many('res.users', string='Force Assigned Users'),
        'user_ids': fields.one2many('project.user.allocation', 'phase_id', "Assigned Users",
                                    states={'confirmed':[('readonly',True)], 'done':[('readonly',True)], 'cancelled':[('readonly',True)]},
                                    help="The resources on the project can be computed automatically by the scheduler."),
        'state': fields.selection([('draft', 'New'),
                                   ('cancelled', 'Cancelled'),
                                   ('confirmed', 'Confermato'),
                                   ('open', 'In Progress'),
                                   ('pending', 'Pending'),
                                   ('done', 'Done')], 'Status',
                                  readonly=True,
                                  required=True,
                                  help='If the phase is created the status \'Draft\'.\n If the phase is started, the status becomes \'In Progress\'.\n If review is needed the phase is in \'Pending\' status.\
                                  \n If the phase is over, the status is set to \'Done\'.'),
        'progress': fields.function(_compute_progress, string='Progress', help="Computed based on related tasks"),
     }
    _defaults = {
        'state': 'draft',
        'sequence': 10,
        'product_uom': _get_product_uom,
        'duration': 0.0,
    }
    _order = "project_id, date_start, sequence"
    _constraints = [
        (_check_recursion, 'Loops in phases not allowed', ['next_phase_ids', 'previous_phase_ids']),
        (_check_dates, 'Phase start-date must be lower than phase end-date.', ['date_start', 'date_end']),
    ]

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if not default.get('name', False):
            default.update(name=_('%s (copy)') % (self.browse(cr, uid, id, context=context).name))
        return super(project_phase, self).copy(cr, uid, id, default, context)

    def set_draft(self, cr, uid, ids, context):
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def set_open(self, cr, uid, ids, context):
        self.write(cr, uid, ids, {'state': 'open'})
        return True

    def set_pending(self, cr, uid, ids, context):
        self.write(cr, uid, ids, {'state': 'pending'})
        return True

    def set_cancel(self, cr, uid, ids, context):
        self.write(cr, uid, ids, {'state': 'cancelled'})
        return True

    def set_done(self, cr, uid, ids, context):
        self.write(cr, uid, ids, {'state': 'done'})
        return True

    def set_confirmed(self, cr, uid, ids, context):
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True
