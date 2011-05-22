"""Detalle de Item Rest Controller Info"""
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

#__all__ = ['DetalleItemRestController']

class DetalleItemRestController(RestController):
    
    @expose('sgs.templates.desarrollo.detalle_item.list')
    def list(self, **kw):
        tmpl_context.widget = list_detalleitem
        value = list_detalleitem_filler.get_value()
        return dict(value=value)


    @expose('sgs.templates.desarrollo.detalle_item.new')
    def new(self, **kw):
        tmpl_context.widget = new_detalleitem_form
        return dict(value=kw)


    @validate(new_detalleitem_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        detalleitem = DetalleItem(**kw)
        DBSession.add(detalleitem)
        flash('Detalle de item creado')
        redirect('/desarrollo/detalle_item/list')


    @expose('sgs.templates.desarrollo.detalle_item.edit')
    def edit(self, id,**kw):
        detalleitem = DBSession.query(DetalleItem).get(id)
        tmpl_context.widget = edit_detalleitem_form
        kw['id_detalleitem'] = detalleitem.id_detalleitem
        kw['id_item'] = detalleitem.id_item
        kw['nombre_atributo'] = detalleitem.nombre_atributo
        kw['tipo_dato'] = detalleitem.tipo_dato
        kw['valor'] = detalleitem.valor
        return dict(value=kw)


    @validate(edit_detalleitem_form, error_handler=edit)
    @expose()
    def put(self, id='', **kw):
        del kw['sprox_id']
        detalleitem = DBSession.query(DetalleItem).get(int(id))
        detalleitem.nombre_atributo = kw['nombre_atributo']
        detalleitem.tipo_dato = kw['tipo_dato']
        detalleitem.valor = kw['valor']
        DBSession.merge(detalleitem)
        flash('Detalle item modificado')
        redirect("/desarrollo/detalle_item/list")


    @expose()
    def post_delete(self, id, **kw):
        DBSession.delete(DBSession.query(DetalleItem).get(id))
        redirect('/desarrollo/detalle_item/list')

