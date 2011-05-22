"""Usuario Controller Info"""
import pylons
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *
from tg import tmpl_context
from repoze.what import predicates


__all__ = ['UsuarioRestController']

class UsuarioRestController(RestController):

	@expose('sgs.templates.administracion.usuario.list')
	@require(predicates.has_permission('ver_usuario_todos'))
	def list(self, **kw):
		tmpl_context.widget = list_usuario
		value = list_usuario_filler.get_value()
		return dict(value=value)


	@expose('sgs.templates.administracion.usuario.new')
	@require(predicates.has_permission('crear_usuario'))
	def new(self, **kw):
		tmpl_context.widget = new_usuario_form
		return dict(value=kw)

	@validate(new_usuario_form, error_handler=new)
	@expose()
	def post(self, _method='', **kw):
		del kw['sprox_id']
		usuario = Usuario()
		usuario.cod_usuario = kw['cod_usuario']
		usuario.nombre = kw['nombre']
		usuario.user_name = kw['user_name']
		usuario.password = kw['password']
		#usuario.groups = []
		
		#for i in kw['proyect']:
		#	p = DBSession.query(Proyecto).get(i)
		#	usuario.proyect.append(p)

		for i in kw['groups']:
			p = DBSession.query(Rol).get(i)
			usuario.groups.append(p)
		DBSession.add(usuario)
		flash('Usuario creado')
		redirect('/administracion/usuario/list')

	@expose('sgs.templates.administracion.usuario.edit')
	@require(predicates.has_permission('editar_usuario'))
	def edit(self, id,**kw):
		usuario = DBSession.query(Usuario).get(id)
		tmpl_context.widget = edit_usuario_form
		kw['id_usuario'] = usuario.id_usuario
		#kw['cod_usuario'] = usuario.cod_usuario
		#kw['nombre'] = usuario.nombre
		#kw['user_name'] = usuario.user_name
		#kw['_password'] = usuario._password
		#kw['password'] = usuario.password
		#kw['proyect'] = usuario.proyect
		#kw['groups'] = usuario.groups
		value=edit_usuario_filler.get_value(kw)
		return dict(value=value)


	@validate(edit_usuario_form, error_handler=edit)
	@require(predicates.has_permission('editar_usuario'))
	@expose()
	def put(self, id='', **kw):
		del kw['sprox_id']
		usuario = DBSession.query(Usuario).get(int(id))
		usuario.nombre = kw['nombre']        
		usuario.user_name = kw['user_name']
		usuario.password = kw['password']

		#for i in kw['proyect']:
		#	p = DBSession.query(Proyecto).get(i)
		#	usuario.proyect.append(p)

		usuario.groups=[]
		for i in kw['groups']:
			p = DBSession.query(Rol).get(i)
			usuario.groups.append(p)

		DBSession.merge(usuario)
		flash('Usuario modificado')
		redirect("/administracion/usuario/list")


	@require(predicates.has_permission('eliminar_usuario'))
	@expose()
	def post_delete(self, id, **kw):
		DBSession.delete(DBSession.query(Usuario).get(id))
		redirect('/administracion/usuario/list')





