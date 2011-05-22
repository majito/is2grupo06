"""Tipo de Item Rest Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *


#__all__ = ['TipoItemRestController']

class TipoItemRestController(RestController):

    @expose('sgs.templates.desarrollo.tipo_item.list')
    def list(self):
        tmpl_context.widget = list_tipoitem
        value = list_tipoitem_filler.get_value()
        return dict(value=value)


    @expose('sgs.templates.desarrollo.tipo_item.new')
    def new(self, **kw):
        tmpl_context.widget = new_tipoitem_form
        return dict(value=kw)


    @validate(new_tipoitem_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        tipoitem = TipoItem(**kw)
        DBSession.add(tipoitem)
        flash('Tipo de item creado')
        redirect('/desarrollo/tipo_item/list')


    @expose('sgs.templates.desarrollo.tipo_item.edit')
    def edit(self, id,**kw):
        tipoitem = DBSession.query(TipoItem).get(id)
        tmpl_context.widget = edit_tipoitem_form
        kw['id_tipoitem'] = tipoitem.id_tipoitem
        kw['cod_tipoitem'] = tipoitem.cod_tipoitem
        kw['nombre_tipoitem'] = tipoitem.nombre_tipoitem
        kw['descripcion'] = tipoitem.descripcion
        kw['fase'] = tipoitem.fase
        return dict(value=kw)


    @validate(edit_tipoitem_form, error_handler=edit)
    @expose()
    def put(self, _method='', id=0, **kw):
        del kw['sprox_id']
        tipoitem = DBSession.query(TipoItem).get(int(id))
        tipoitem.nombre_tipoitem = kw['nombre_tipoitem']
        tipoitem.descripcion = kw['descripcion']
        DBSession.merge(tipoitem)
        flash('Tipo de Item modificado')
        redirect("/desarrollo/tipo_item/list")


    @expose()
    def post_delete(self, id, **kw):
        DBSession.delete(DBSession.query(TipoItem).get(id))
        redirect('/desarrollo/tipo_item/list')


