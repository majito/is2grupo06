"""Linea Base Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from tg import expose, flash, require, url, request, redirect, validate

from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *
import time


#__all__ = ['LineaBaseRestController']

class LineaBaseRestController(RestController):

	id_fase = 0
	
	@expose('sgs.templates.configuracion.linea_base.list')
	def list(self, id_fase):
		
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			listar = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="ver_linea_base").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if (len(listar)==0):
				flash("No posee los permisos para ver las lineas bases",'error')
				redirect("/configuracion/linea_base/error")
			else:
				self.id_fase = id_fase
				fase = DBSession.query(Fase).get(id_fase)
				tmpl_context.widget = list_lineabase
				value = list_lineabase_filler.get_value(id_fase=id_fase)
		else:
			self.id_fase = id_fase
			fase = DBSession.query(Fase).get(id_fase)
			tmpl_context.widget = list_lineabase
			value = list_lineabase_filler.get_value(id_fase=id_fase)
		return dict(fase=fase, value=value)
	
	
	@expose('sgs.templates.configuracion.linea_base.new')
	def new(self, id_fase, method='', **kw):
		
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			crear = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="crear_linea_base").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if len(crear)==0:
				flash("No posee los permisos para crear linea base",'error')
				redirect("/configuracion/linea_base/error")
			else:
				ItemsFieldSelect.id_fase = id_fase
				new_lineabase_form = NewLineaBaseForm(DBSession)#new_lineabase_form
				tmpl_context.widget = new_lineabase_form
		else:
			ItemsFieldSelect.id_fase = id_fase
			new_lineabase_form = NewLineaBaseForm(DBSession)#new_lineabase_form
			tmpl_context.widget = new_lineabase_form
		return dict(value=kw)


	#@validate(new_lineabase_form, error_handler=new)
	@expose()
	def post(self, id_fase, method='', **kw):
		del kw['sprox_id']
		lineabase = LineaBase()
		lineabase.cod_lb = kw['cod_lb']
		lineabase.estado = "cerrado"
		lineabase.id_fase = id_fase 
		#id_fa = id_fase
		for i in kw['item']:
			p = DBSession.query(Item).get(i)
			lineabase.item.append(p)
		
		items = []
		tipos = DBSession.query(TipoItem.id_tipoitem).filter(TipoItem.id_fase == id_fase).all()
		for i in tipos:
			item = DBSession.query(Item.id_item).filter(Item.id_tipoitem==i).all()
			items.extend(item)
		
		if (len(items) == len(kw['item'])):
			lineabase.tipo = "total"
		else:
			lineabase.tipo = "parcial"
		DBSession.add(lineabase)
		lb = DBSession.query(LineaBase.id_lb).filter(LineaBase.id_fase==id_fase).all() 
		if (lb is not None):
			for j in lb:
				linea = DBSession.query(LineaBase).get(j)
				if (linea.id_lb != lineabase.id_lb and linea.tipo == "total"):
					linea.tipo = "parcial"
					DBSession.merge(linea)
		DBSession.flush()
		
		for i in kw['item']:
			p = DBSession.query(Item).get(i)
			p.id_lb = lineabase.id_lb
			DBSession.merge(p)
			
			
		
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		ahora = time.localtime()
		
		anho = str(ahora.tm_year)
		mes = str(ahora.tm_mon)
		dia = str(ahora.tm_mday)
		hora = str(ahora.tm_hour)
		min = str(ahora.tm_min)
		seg = str(ahora.tm_sec)
		historial = Historial()
		historial.cod_recurso = lineabase.cod_lb
		historial.tipo_recurso = "Linea_Base"
		historial.nombre_recurso = "sinNombre"
		historial.operacion = "Creacion"
		historial.fecha_operacion = anho+'-'+mes+'-'+dia
		historial.hora = hora+':'+min+':'+seg
		historial.nombre_usuario = user.user_name
		DBSession.add(historial)
		
		flash('Linea Base creada')
		redirect('/configuracion/linea_base/list/'+str(lineabase.id_fase))


	@expose()
	def abrir(self, id, **kw):
		
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		id_fase = DBSession.query(LineaBase.id_fase).filter(LineaBase.id_lb==id).one()
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			abrir = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="abrir_linea_base").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if len(abrir)==0:
				flash("No posee los permisos para abrir linea base",'error')
				redirect("/configuracion/linea_base/error")
			else:
				lineabase = DBSession.query(LineaBase).get(id)
				lineabase.estado = "abierto"
				DBSession.merge(lineabase)
				
				items = DBSession.query(Item).filter(Item.id_lb==id).all()
				print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+str(len(items)) 
				for i in items:
					i.estado = "revision"
					DBSession.merge(i)
				identity = request.environ.get('repoze.who.identity')
				if identity is not None:
					user = identity.get('user')
				idi = user.id_usuario
				
				ahora = time.localtime()
				
				anho = str(ahora.tm_year)
				mes = str(ahora.tm_mon)
				dia = str(ahora.tm_mday)
				hora = str(ahora.tm_hour)
				min = str(ahora.tm_min)
				seg = str(ahora.tm_sec)
				historial = Historial()
				historial.cod_recurso = lineabase.cod_lb
				historial.tipo_recurso = "Linea_Base"
				historial.nombre_recurso = "sinNombre"
				historial.operacion = "Apertura"
				historial.fecha_operacion = anho+'-'+mes+'-'+dia
				historial.hora = hora+':'+min+':'+seg
				historial.nombre_usuario = user.user_name
				DBSession.add(historial)
				
				
				
				flash('Linea Base Abierta')
				redirect('/configuracion/linea_base/list/'+str(lineabase.id_fase))
		else:
			lineabase = DBSession.query(LineaBase).get(id)
			lineabase.estado = "abierto"
			DBSession.merge(lineabase)
			
			items = DBSession.query(Item).filter(Item.id_lb==id).all()
			print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"+str(len(items)) 
			for i in items:
				i.estado = "revision"
				DBSession.merge(i)
			
			identity = request.environ.get('repoze.who.identity')
			if identity is not None:
				user = identity.get('user')
			idi = user.id_usuario
			
			ahora = time.localtime()
			
			anho = str(ahora.tm_year)
			mes = str(ahora.tm_mon)
			dia = str(ahora.tm_mday)
			hora = str(ahora.tm_hour)
			min = str(ahora.tm_min)
			seg = str(ahora.tm_sec)
			historial = Historial()
			historial.cod_recurso = lineabase.cod_lb
			historial.tipo_recurso = "Linea_Base"
			historial.nombre_recurso = "sinNombre"
			historial.operacion = "Apertura"
			historial.fecha_operacion = anho+'-'+mes+'-'+dia
			historial.hora = hora+':'+min+':'+seg
			historial.nombre_usuario = user.user_name
			DBSession.add(historial)
			
			flash('Linea Base Abierta')
			redirect('/configuracion/linea_base/list/'+str(lineabase.id_fase))

