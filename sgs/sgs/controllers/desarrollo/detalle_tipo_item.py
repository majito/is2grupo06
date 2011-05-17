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


#from sprox.formbase import AddRecordForm

#__all__ = ['TipoItemRestController']

class DetalleTipoItemRestController(RestController):


    @expose('sgs.templates.desarrollo.detalle_tipo_item.list')
    def list(self, **kw):
        tmpl_context.widget = list_detalletipoitem
        value = list_detalletipoitem_filler.get_value()
        return dict(value=value)


    @expose('sgs.templates.desarrollo.detalle_tipo_item.new')
    def new(self, **kw):
        tmpl_context.widget = new_detalletipoitem_form
        return dict(value=kw)


    @validate(new_detalletipoitem_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        detalletipoitem = DetalleTipoItem(**kw)
        DBSession.add(detalletipoitem)
        flash('Detalle de Tipo de item creado')
        redirect('/desarrollo/detalle_tipo_item/list')


    @expose('sgs.templates.desarrollo.detalle_tipo_item.edit')
    def edit(self, id,**kw):
        detalletipoitem = DBSession.query(DetalleTipoItem).get(id)
        tmpl_context.widget = edit_detalletipoitem_form
        kw['id_detalletipoitem'] = detalletipoitem.id_detalletipoitem
        kw['id_tipoitem'] = detalletipoitem.id_tipoitem
        kw['nombre_atributo'] = detalletipoitem.nombre_atributo
        kw['tipo_dato'] = detalletipoitem.tipo_dato
        return dict(value=kw)


    @validate(edit_detalletipoitem_form, error_handler=edit)
    @expose()
    def put(self, _method='', id=0, **kw):
        del kw['sprox_id']
        detalletipoitem = DetalleTipoItem(**kw)
        DBSession.merge(detalletipoitem)
        flash('Detalle de Tipo de item modificado')
        redirect("/desarrollo/detalle_tipo_item/list")


    @expose()
    def post_delete(self, id, **kw):
        DBSession.delete(DBSession.query(DetalleTipoItem).get(id))
        redirect('/desarrollo/detalle_tipo_item/list')


