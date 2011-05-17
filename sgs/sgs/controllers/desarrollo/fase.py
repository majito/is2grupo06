"""Fase Rest Controller Info"""
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

#__all__ = ['FaseRestController']

class FaseRestController(RestController):

    @expose('sgs.templates.desarrollo.fase.list')
    def list(self):
        tmpl_context.widget = list_fase
        value = list_fase_filler.get_value()
        return dict(value=value)


    @expose('sgs.templates.desarrollo.fase.new')
    def new(self, **kw):
        tmpl_context.widget = new_fase_form
        return dict(value=kw)


    @validate(new_fase_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        fase = Fase(**kw)
        DBSession.add(fase)
        flash('Fase creada')
        redirect('/desarrollo/fase/list')


    @expose('sgs.templates.desarrollo.fase.edit')
    def edit(self, id,**kw):
        fase = DBSession.query(Fase).get(id)
        tmpl_context.widget = edit_fase_form
        kw['id_fase'] = fase.id_fase
        kw['cod_fase'] = fase.cod_fase
        kw['nombre_fase'] = fase.nombre_fase
        kw['descripcion'] = fase.descripcion
        return dict(value=kw)


    @validate(edit_fase_form, error_handler=edit)
    @expose()
    def put(self, _method='', id=0, **kw):
        del kw['sprox_id']
        fase = Fase(**kw)
        DBSession.merge(fase)
        flash('Fase modificada')
        redirect("/desarrollo/fase/list")


    @expose()
    def post_delete(self, id, **kw):
        DBSession.delete(DBSession.query(Fase).get(id))
        redirect('/desarrollo/fase/list')
   


