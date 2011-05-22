"""Proyecto Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *
from repoze.what import predicates


#__all__ = ['ProyectoRestController']

class ProyectoRestController(RestController):


	@expose('sgs.templates.administracion.proyecto.list')
	@require(predicates.has_permission('ver_proyecto_todos'))
	def list(self):
		tmpl_context.widget = list_proyecto
		value = list_proyecto_filler.get_value()
		return dict(value=value)


	@expose('sgs.templates.administracion.proyecto.new')
	@require(predicates.has_permission('crear_proyecto'))
	def new(self, **kw):
		tmpl_context.widget = new_proyecto_form
		return dict(value=kw)


	@validate(new_proyecto_form, error_handler=new)
	@expose()
	def post(self, _method='', **kw):
		del kw['sprox_id']
		proyecto = Proyecto()
		#proyecto.id_proyecto = kw['id_proyecto']
		proyecto.cod_proyecto = kw['cod_proyecto']
		proyecto.nombre_proyecto = kw['nombre_proyecto']
		proyecto.descripcion = kw['descripcion']
		proyecto.fecha_inicio = kw['fecha_inicio']
		#proyecto.proyectos=[]
		for i in kw['usuarios'] :
			p = DBSession.query(Usuario).get(i)
			proyecto.usuarios.append(p)
			#rol.permissions.append(DBSession.query(Permiso).get(permiso))

		#kw['permissions'] = permisos

		#rol = Rol(**kw)
		DBSession.add(proyecto)
		flash('Proyecto creado')
		redirect('/administracion/proyecto/list')


	@expose('sgs.templates.administracion.proyecto.edit')
	@require(predicates.has_permission('editar_proyecto'))
	def edit(self, id,**kw):
		proyecto = DBSession.query(Proyecto).get(id)
		tmpl_context.widget = edit_proyecto_form
		kw['id_proyecto'] = proyecto.id_proyecto
		#kw['cod_proyecto'] = proyecto.cod_proyecto
		#kw['nombre_proyecto'] = proyecto.nombre_proyecto
		#kw['descripcion'] = proyecto.descripcion
		#kw['fecha_inicio'] = proyecto.fecha_inicio
		value = edit_proyecto_filler.get_value(kw)
		return dict(value=value)


	@validate(edit_proyecto_form, error_handler=edit)
	@expose()
	def put(self, id='', **kw):
		del kw['sprox_id']
		proyecto = DBSession.query(Proyecto).get(id)
		proyecto.nombre_proyecto = kw['nombre_proyecto']
		proyecto.descripcion = kw['descripcion']
		proyecto.fecha_inicio = kw['fecha_inicio']
		proyecto.usuarios=[]
		for i in kw['usuarios'] :
			p = DBSession.query(Usuario).get(i)
			proyecto.usuarios.append(p)

		DBSession.merge(proyecto)
		flash('Proyecto modificado')
		redirect("/administracion/proyecto/list")


	@require(predicates.has_permission('eliminar_proyecto'))
	@expose()
	def post_delete(self, id, **kw):
		DBSession.delete(DBSession.query(Proyecto).get(id))
		redirect('/administracion/proyecto/list')
