"""Item Rest Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *


#__all__ = ['ItemRestController']

class ItemRestController(RestController):

    @expose('sgs.templates.desarrollo.item.list')
    def list(self):
        tmpl_context.widget = list_item
        value = list_item_filler.get_value()
        return dict(value=value)


    @expose('sgs.templates.desarrollo.item.new')
    def new(self, **kw):
        tmpl_context.widget = new_item_form
        return dict(value=kw)


    @validate(new_item_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        item = Item(**kw)
        DBSession.add(item)
        flash('Item creado')
        redirect('/desarrollo/item/list')


    @expose('sgs.templates.desarrollo.item.edit')
    def edit(self, id,**kw):
        item = DBSession.query(Item).get(id)
        tmpl_context.widget = edit_item_form
        kw['id_item'] = item.id_item
        kw['cod_item'] = item.cod_item
        kw['nombre_item'] = item.nombre_item
        kw['descripcion'] = item.descripcion
        kw['version'] = item.version
        kw['estado'] = item.estado
        kw['complejidad'] = item.complejidad
        return dict(value=kw)


    @validate(edit_item_form, error_handler=edit)
    @expose()
    def put(self, _method='', id=0, **kw):
        del kw['sprox_id']
        item = DBSession.query(Item).get(id)
        item.nombre_item = kw['nombre_item']
        item.descripcion = kw['descripcion']
        item.estado = kw['estado']
        DBSession.merge(item)
        flash('Item modificado')
        redirect("/desarrollo/item/list")


    @expose()
    def post_delete(self, id, **kw):
        DBSession.delete(DBSession.query(Item).get(id))
        redirect('/desarrollo/item/list')





