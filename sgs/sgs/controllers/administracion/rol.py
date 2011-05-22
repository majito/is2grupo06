"""Rol Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *


#__all__ = ['RolRestController']

class RolRestController(RestController):

	@expose('sgs.templates.administracion.rol.list')
	def list(self):
		tmpl_context.widget = list_rol
		value = list_rol_filler.get_value()
		return dict(value=value)


	@expose('sgs.templates.administracion.rol.new')
	def new(self, **kw):
		tmpl_context.widget = new_rol_form
		return dict(value=kw)


	@validate(new_rol_form, error_handler=new)
	@expose()
	def post(self, _method='', **kw):
		del kw['sprox_id']
		#rol = DBSession.query(Rol).get(id)
		rol = Rol()
		#rol.id_rol = kw['id_rol']
		rol.cod_rol = kw['cod_rol']
		rol.group_name = kw['group_name']
		rol.descripcion = kw['descripcion']
		#rol.permissions=[]
		for i in kw['permissions']:
			p = DBSession.query(Permiso).get(i)
			rol.permissions.append(p)
			#rol.permissions.append(DBSession.query(Permiso).get(permiso))
		#kw['permissions'] = permisos
		#rol = Rol(**kw)
		DBSession.add(rol)
		flash('Rol creado')
		redirect('/administracion/rol/list')

	@expose('sgs.templates.administracion.rol.edit')
	def edit(self, id,**kw):
		rol = DBSession.query(Rol).get(id)
		tmpl_context.widget = edit_rol_form
		kw['id_rol'] = rol.id_rol
		#kw['cod_rol'] = rol.cod_rol
		#kw['group_name'] = rol.group_name
		#kw['descripcion'] = rol.descripcion
		#kw['permissions'] = rol.permissions
		value = edit_rol_filler.get_value(kw)
		return dict(value=value)


	@validate(edit_rol_form, error_handler=edit)
	@expose()
	def put(self, id='', **kw):
		del kw['sprox_id']
		rol = DBSession.query(Rol).get(int(id))
		rol.group_name = kw['group_name']
		rol.descripcion = kw['descripcion']
		rol.permissions=[]
		for i in kw['permissions'] :
			p = DBSession.query(Permiso).get(i)
			rol.permissions.append(p)
		DBSession.merge(rol)
		flash('Rol modificado')
		redirect("/administracion/rol/list")


	@expose()
	def post_delete(self, id, **kw):
		DBSession.delete(DBSession.query(Rol).get(id))
		redirect('/administracion/rol/list')
