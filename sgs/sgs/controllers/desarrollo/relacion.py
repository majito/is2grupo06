"""Relacion Rest Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *


#from sprox.formbase import AddRecordForm

#__all__ = ['RelacionRestController']

class RelacionRestController(RestController):

    @expose('sgs.templates.desarrollo.relacion.list')
    def list(self):
        tmpl_context.widget = list_relacion
        value = list_relacion_filler.get_value()
        return dict(value=value)


    @expose('sgs.templates.desarrollo.relacion.new')
    def new(self, **kw):
        tmpl_context.widget = new_relacion_form
        return dict(value=kw)


    @validate(new_relacion_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        relacion = Relacion(**kw)
        DBSession.add(relacion)
        flash('Relacion creada')
        redirect('/desarrollo/relacion/list')


    @expose('sgs.templates.desarrollo.relacion.edit')
    def edit(self, id,**kw):
        relacion = DBSession.query(Relacion).get(id)
        tmpl_context.widget = edit_relacion_form
        kw['id_relacion'] = relacion.id_relacion
        kw['cod_relacion'] = relacion.cod_relacion
        kw['descripcion'] = relacion.descripcion
        kw['tiporelacion'] = relacion.tiporelacion
        return dict(value=kw)


    @validate(edit_relacion_form, error_handler=edit)
    @expose()
    def put(self, id='', **kw):
        del kw['sprox_id']
        relacion = DBSession.query(Relacion).get(int(id))
        relacion.descripcion = kw['descripcion']
        relacion.tiporelacion = kw['tiporelacion']
        DBSession.merge(relacion)
        flash('Relacion modificada')
        redirect("/desarrollo/relacion/list")


    @expose()
    def post_delete(self, id, **kw):
        DBSession.delete(DBSession.query(Relacion).get(id))
        redirect('/desarrollo/relacion/list')



