"""Usuario Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *
from tg import tmpl_context


#from sprox.formbase import AddRecordForm

__all__ = ['UsuarioRestController']

class UsuarioRestController(RestController):


    @expose('sgs.templates.administracion.usuario.new')
    def new(self, **kw):
        tmpl_context.widget = new_usuario_form
        return dict(value=kw)

    @validate(new_usuario_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        usuario = Usuario(**kw)
        DBSession.add(usuario)
        flash('Usuario creado')
        redirect('/administracion/usuario/list')

    @expose('sgs.templates.administracion.usuario.edit')
    def edit(self, id,**kw):
        usuario = DBSession.query(Usuario).get(id)
        tmpl_context.widget = edit_usuario_form
        kw['id_usuario'] = usuario.id_usuario
        kw['cod_usuario'] = usuario.cod_usuario
        kw['nombre_usuario'] = usuario.nombre_usuario
        kw['contrasena'] = usuario.contrasena
        kw['nombre'] = usuario.nombre
        kw['apellido'] = usuario.apellido
        kw['fecha_nacimiento'] = usuario.fecha_nacimiento
        kw['genero'] = usuario.genero
        return dict(value=kw)


    @validate(edit_usuario_form, error_handler=edit)
    @expose()
    def put(self, _method='', **kw):
        del kw['sprox_id']
        usuario = Usuario(**kw)
        DBSession.merge(usuario)
        flash('Usuario modificado')
        redirect("/administracion/usuario/list")


    @expose('sgs.templates.administracion.usuario.list')
    def list(self, **kw):
        tmpl_context.widget = list_usuario
        value = list_usuario_filler.get_value()
        return dict(value=value)



