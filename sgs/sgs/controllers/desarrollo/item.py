"""Item Rest Controller"""
from sgs.controllers.udf import *
from datetime import datetime
from tg.controllers import RestController, redirect
from tg import expose, flash, require, url, request, redirect, validate
from tg.decorators import paginate
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *
from sgs.form.edit import *

#import de la libreria de grafo
from pygraph.classes.digraph import *
from pygraph.algorithms.cycles import *
from pygraph.readwrite.dot import write
import time

# Import graphviz
import sys
import _gv
import pydot

class ItemRestController(RestController):

	id_fase=0
	@expose('sgs.templates.desarrollo.item.list')
	@paginate("value", items_per_page=6)
	@require(predicates.has_permission('ver_fase'))
	def list(self, id_fase):
		"""Metodo invocado para listar los items de una fase especificada"""
		self.id_fase = id_fase
		
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		fase = DBSession.query(Fase).get(id_fase)
		id_proy = fase.id_proyecto
		proyecto = DBSession.query(Proyecto).get(id_proy)
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			list = DBSession.query(Roperpro).filter(Roperpro.id_proyecto==id_proy).\
											filter(Permiso.permission_name=="ver_fase").\
											filter(Roperpro.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).\
											filter(Roperpro.id_rol==RolUsuario.id_rol).all()
			if len(list)==0:
				flash("No posee el permiso para ver los items de la fase",'error')
				redirect("/desarrollo/item/error")
			else:
				fase = DBSession.query(Fase).get(id_fase)
				tmpl_context.widget = list_item
				value = list_item_filler.get_value(id_fase=id_fase)
		else:
			fase = DBSession.query(Fase).get(id_fase)
			tmpl_context.widget = list_item
			value = list_item_filler.get_value(id_fase=id_fase)
		return dict(fase=fase, proyecto = proyecto, value=value)


	@expose('sgs.templates.desarrollo.item.new')
	@require(predicates.has_permission('crear_item'))
	def new(self, id_fase, method='', **kw):
		"""Metodo que trae el formulario para crear un item nuevo"""
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			crear = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="crear_item").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if len(crear)==0:
				flash("No posee los permisos para crear item en la fase",'error')
				redirect("/desarrollo/item/error")
			else:
				new_item_form.tipo_item.id_fase = id_fase
				tmpl_context.widget = new_item_form
		else:
			new_item_form.tipo_item.id_fase = id_fase
			tmpl_context.widget = new_item_form
		return dict(id_fase = id_fase, value=kw)


	@validate(new_item_form, error_handler=new)
	@require(predicates.has_permission('crear_item'))
	@expose()
	def post(self, id_fase, method='', **kw):
		"""Metodo invocado para persistir los datos del item creado en la BD"""
		del kw['sprox_id']
		funciones = Funciones()
		item = Item()
		item.id_tipoitem = kw['tipo_item']
		tipoitem = DBSession.query(TipoItem).filter(TipoItem.id_tipoitem==item.id_tipoitem).first()
		cod_tipoitem = tipoitem.cod_tipoitem
		item.cod_item = str(cod_tipoitem)+str(funciones.generador_codigo_item(cod_tipoitem))
		item.nombre_item = kw['nombre_item']
		item.descripcion = kw['descripcion']
		item.version = 1#kw['version']
		item.estado = "en desarrollo"
		item.complejidad = kw['complejidad']

		id_fa = id_fase

		item.id_tipoitem = kw['tipo_item']
		
		DBSession.add(item)
		DBSession.flush()
		#VERSIONADO_ITEM
		cod_tipoitem_versionado = DBSession.query(TipoItem.cod_tipoitem).filter(TipoItem.id_tipoitem==item.id_tipoitem).first()
		
		versionadoitem = VersionadoItem()
		versionadoitem.cod_item = item.cod_item
		versionadoitem.cod_tipoitem= cod_tipoitem_versionado
		versionadoitem.nombre_item = item.nombre_item
		versionadoitem.descripcion = item.descripcion
		versionadoitem.version = item.version
		versionadoitem.complejidad = item.complejidad
		
		DBSession.add(versionadoitem)
		DBSession.flush()
		print ("0000000000000000000000000000000000000000000000000000000000000000 VERSIONADO %s") % (versionadoitem.id_versionado)
		
		#se crean los detalles del item en base a los detalles del tipo
		detalles = DBSession.query(DetalleTipoItem.id_detalletipoitem).filter(DetalleTipoItem.id_tipoitem==kw['tipo_item']).all()
		
		for i in detalles:
			detalle = DBSession.query(DetalleTipoItem).get(i)
			atributo = DetalleItem()
			atributo.id_item = item.id_item
			atributo.tipo_dato = DBSession.query(DetalleTipoItem.tipo_dato).filter(DetalleTipoItem.id_detalletipoitem==i).first()
			atributo.id_detalletipoitem = i
			atributo.cod_detalleitem = funciones.generador_codigo(detalle.nombre_atributo)
			atributo.cod_detalletipoitem = DBSession.query(DetalleTipoItem.cod_detalletipoitem).filter(DetalleTipoItem.id_detalletipoitem==i).first()
			atributo.nombre_atributo = detalle.nombre_atributo
			atributo.valor = None
			#atributo.archivo = None
			DBSession.add(atributo)
			
			#DETALLE_VERSIONADO_ITEM
			detalleversionadoitem = DetalleVersionadoItem()
			detalleversionadoitem.id_versionado = versionadoitem.id_versionado
			detalleversionadoitem.cod_item = item.cod_item
			detalleversionadoitem.cod_detalleitem = atributo.cod_detalleitem
			detalleversionadoitem.cod_detalletipoitem = atributo.cod_detalletipoitem
			detalleversionadoitem.nombre_atributo = detalle.nombre_atributo
			detalleversionadoitem.tipo_dato = atributo.tipo_dato
			detalleversionadoitem.valor = None
			#detalleversionadoitem.archivo = atributo.archivo
			DBSession.add(detalleversionadoitem)
			
		
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
		historial.cod_recurso = item.cod_item
		historial.tipo_recurso = "Item"
		historial.nombre_recurso = item.nombre_item
		historial.operacion = "Creacion"
		historial.fecha_operacion = anho+'-'+mes+'-'+dia
		historial.hora = hora+':'+min+':'+seg
		historial.nombre_usuario = user.user_name
		DBSession.add(historial)
		
		flash('Item creado')
		redirect('/desarrollo/item/list/'+str(id_fa))


	@expose('sgs.templates.desarrollo.item.edit')
	@require(predicates.has_permission('editar_item'))
	def edit(self, id,**kw):
		"""Metodo para editar un item"""
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
		
			id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
			id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one()
			
			editar = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="editar_item").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if len(editar)==0:
				flash("No posee los permisos para editar los items de la fase",'error')
				redirect("/desarrollo/item/error")
			else:#********************************************************************************************desde aca
				item = DBSession.query(Item).get(id)
				ide_lb = DBSession.query(ItemLineaBase.id_lb).filter(ItemLineaBase.id_item==id).first()
				print ("0000000000000000000000000000000000000000000000000000000 %d") % (ide_lb)
				if ide_lb is not None:
					estado_lb = DBSession.query(LineaBase.estado).filter(LineaBase.id_lb==ide_lb).one()
					if (estado_lb != "cerrado"):
						id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
						id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one()
						#edit_item_form.tipo_item.id_fase = id_fase
						tmpl_context.widget = edit_item_form
						kw['id_item'] = item.id_item
						value = edit_item_filler.get_value(kw)
					else:
						if (estado_lb == "cerrado"):
							ide_lb = DBSession.query(Item.id_lb).filter(Item.id_item==id).one()
							id_fa = DBSession.query(LineaBase.id_fase).filter(LineaBase.id_lb==ide_lb).one() ######
							flash("El item pertenece a una Linea Base cerrada",'error')
							redirect("/desarrollo/item/error")
						#~ redirect('/desarrollo/item/list/'+str(id_fa))
				else:
					item = DBSession.query(Item).get(id)
					id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
					id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one()
					#edit_item_form.tipo_item.id_fase = id_fase
					tmpl_context.widget = edit_item_form
					kw['id_item'] = item.id_item
					value = edit_item_filler.get_value(kw)
		else:
			item = DBSession.query(Item).get(id) # if para controlar...
			ide_lb = DBSession.query(ItemLineaBase.id_lb).filter(ItemLineaBase.id_item==id).first()
			if ide_lb is not None:
				id_fase = DBSession.query(LineaBase.id_fase).filter(LineaBase.id_lb==ide_lb).one()
				estado_lb = DBSession.query(LineaBase.estado).filter(LineaBase.id_lb==ide_lb).one()
				if (estado_lb != "cerrado"):
					id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one() ####
					id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one() ####
					#edit_item_form.tipo_item.id_fase = id_fase
					tmpl_context.widget = edit_item_form
					kw['id_item'] = item.id_item
					value = edit_item_filler.get_value(kw)
				else:
					 if (estado_lb == "cerrado"):
						item = DBSession.query(Item).get(id) ###
						ide_lb = DBSession.query(ItemLineaBase.id_lb).filter(ItemLineaBase.id_item==id).one() ###
						id_fa = DBSession.query(LineaBase.id_fase).filter(LineaBase.id_lb==ide_lb).one() ###
						flash("El item pertenece a una Linea Base cerrada",'error')
						redirect("/desarrollo/item/error")
			else:
				item = DBSession.query(Item).get(id)
				id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
				id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one()
				#edit_item_form.tipo_item.id_fase = id_fase
				tmpl_context.widget = edit_item_form
				kw['id_item'] = item.id_item
				value = edit_item_filler.get_value(kw)
		#~ else:
			#~ item = DBSession.query(Item).get(id)
			#~ id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
			#~ id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one()
			#~ #edit_item_form.tipo_item.id_fase = id_fase
			#~ tmpl_context.widget = edit_item_form
			#~ kw['id_item'] = item.id_item
			#~ value = edit_item_filler.get_value(kw)
		return dict(id_fase=id_fase, value=value)


	@validate(edit_item_form, error_handler=edit)
	@require(predicates.has_permission('editar_item'))
	@expose()
	def put(self, id='', **kw):
		"""Metodo invocado para persistir los datos modificados """
		del kw['sprox_id']
		item = DBSession.query(Item).get(id)
		id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
		id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).all()

		for i in id_fase:
			fase = DBSession.query(Fase).get(i)
		print ("0000000000000000000000000000000000000000000000000000000 version del item en put es: %d") % (item.version)
		item.nombre_item = kw['nombre_item']
		item.descripcion = kw['descripcion']
		item.estado = "revision"
		#item.id_tipoitem = kw['tipo_item']
		item.version = item.version + 1
		item.complejidad = kw['complejidad']
		
		DBSession.merge(item)
		
		""" si el item se encuentra en una linea base, esta debe estar abierta... una vez abierta, debe pasar a estado 
			comprometido
		"""
		#relaciones del item modificado
		list_relaciones = DBSession.query(Relacion.id_relacion).filter(Relacion.id_item1==id).all()
		print ("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww linea base del item en put es: %s") % (list_relaciones)
		for i in list_relaciones:
			iditem = DBSession.query(Relacion.id_item2).filter(Relacion.id_relacion==i).one()
			lb = DBSession.query(ItemLineaBase.id_lb).filter(ItemLineaBase.id_item==iditem).one()
			print ("0000000000000000000000000000000000000000000000000000000 linea base del item en put es: %d") % (lb)
			linea = DBSession.query(LineaBase).filter(LineaBase.id_lb==lb).all()
			for j in linea:
				j.estado = "comprometida"
				DBSession.merge(j)

					
		lb = DBSession.query(ItemLineaBase.id_lb).filter(ItemLineaBase.id_item==id).first()
		if lb is not None:
			print ("0000000000000000000000000000000000000000000000000000000 linea base del item en put es: %d") % (lb)
			linea = DBSession.query(LineaBase).filter(LineaBase.id_lb==lb).all()
			for i in linea:
				i.estado = "comprometida"
				DBSession.merge(i)
		#Aqui se Agrega el registro del item a la taba de versionado
		cod_tipoitem_versionado = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).first()
		
		versionadoitem = VersionadoItem()
		versionadoitem.cod_item = item.cod_item
		versionadoitem.cod_tipoitem= cod_tipoitem_versionado
		versionadoitem.nombre_item = item.nombre_item
		versionadoitem.descripcion = item.descripcion
		versionadoitem.version = item.version
		versionadoitem.complejidad = item.complejidad
		
		DBSession.add(versionadoitem)
		DBSession.flush()

		
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
		historial.cod_recurso = item.cod_item
		historial.tipo_recurso = "Item"
		historial.nombre_recurso = item.nombre_item
		historial.operacion = "Modificacion"
		historial.fecha_operacion = anho+'-'+mes+'-'+dia
		historial.hora = hora+':'+min+':'+seg
		historial.nombre_usuario = user.user_name
		DBSession.add(historial)
		
		flash('Item modificado')
		redirect("/desarrollo/item/list/"+str(fase.id_fase))

	@require(predicates.has_permission('eliminar_item'))
	@expose()
	def post_delete(self, id, **kw):
		"""Metodo invocado para eliminar un item especificado"""
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			eliminar = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="eliminar_item").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if len(list)==0:
				flash("No posee los permisos para eliminar los items de la fase",'error')
				redirect("/desarrollo/item/error")
			else:
				list_relaciones = DBSession.query(Relacion.id_relacion).filter(Relacion.id_item1==id).all()
				for i in list_relaciones:
					DBSession.delete(DBSession.query(Relacion).get(i))
				
				item = DBSession.query(Item).get(int(id))
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
				historial.cod_recurso = item.cod_item
				historial.tipo_recurso = "Item"
				historial.nombre_recurso = item.nombre_item
				historial.operacion = "Eliminacion"
				historial.fecha_operacion = anho+'-'+mes+'-'+dia
				historial.hora = hora+':'+min+':'+seg
				historial.nombre_usuario = user.user_name
				DBSession.add(historial)
				DBSession.delete(DBSession.query(Item).get(id))
				redirect('/desarrollo/item/list/'+str(self.id_fase))
		else:
			list_relaciones = DBSession.query(Relacion.id_relacion).filter(Relacion.id_item1==id).all()
			for i in list_relaciones:
				DBSession.delete(DBSession.query(Relacion).get(i))
				
			item = DBSession.query(Item).get(int(id))
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
			historial.cod_recurso = item.cod_item
			historial.tipo_recurso = "Item"
			historial.nombre_recurso = item.nombre_item
			historial.operacion = "Eliminacion"
			historial.fecha_operacion = anho+'-'+mes+'-'+dia
			historial.hora = hora+':'+min+':'+seg
			historial.nombre_usuario = user.user_name
			DBSession.add(historial)
				
				
			DBSession.delete(DBSession.query(Item).get(id))
			redirect('/desarrollo/item/list/'+str(self.id_fase))

	@expose()
	def aprobar(self, id, **kw):
		"""Metodo invocado para aprobar un item especificado"""
		identity = request.environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
		idi = user.id_usuario
		
		id_tipo = DBSession.query(Item.id_tipoitem).filter(Item.id_item==id).one()
		id_fase = DBSession.query(TipoItem.id_fase).filter(TipoItem.id_tipoitem==id_tipo).one()
		
		rol_lider = DBSession.query(RolUsuario).filter(RolUsuario.id_usuario==idi).\
				filter(Rol.group_name=="lider").filter(Rol.id_rol == RolUsuario.id_rol).all()
		
		if(len(rol_lider)==0):
			aprob = DBSession.query(Usperfa).filter(Usperfa.id_fase==id_fase).\
											filter(Permiso.permission_name=="aprobar_item").\
											filter(Usperfa.id_permiso==Permiso.id_permiso).\
											filter(RolUsuario.id_usuario==idi).all()
			if len(aprob)==0:
				flash("No posee permiso para aprobar item",'error')
				redirect("/desarrollo/item/error")
			else:
				item = DBSession.query(Item).get(id)
				item.estado = "aprobado"
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
				historial.cod_recurso = item.cod_item
				historial.tipo_recurso = "Item"
				historial.nombre_recurso = item.nombre_item
				historial.operacion = "Aprobacion"
				historial.fecha_operacion = anho+'-'+mes+'-'+dia
				historial.hora = hora+':'+min+':'+seg
				historial.nombre_usuario = user.user_name
				DBSession.add(historial)
				flash("Item aprobado")
				redirect('/desarrollo/item/list/'+str(self.id_fase))
		#~ else:
			#~ item = DBSession.query(Item).get(id)
			#~ item.estado = "aprobado"
		else:#*******************************************************************************************desde aca
			item = DBSession.query(Item).get(id)
			item.estado = "aprobado"
			iditem = item.id_item
			
			if (item.id_lb!=None):
				"""Si todos los items de la linea base, que fueron modificados, 
				se aprueban, la linea base se cierra automaticamente"""
				lb = DBSession.query(ItemLineaBase.id_lb).filter(ItemLineaBase.id_item==iditem).one()
				print ("0000000000000000000000000000000000000000000000000000000 linea base del item en put es: %s") % (lb)
				list_items = []
				apro = 0
				list_items = DBSession.query(Item).filter(Item.id_lb==lb).all()
				for k in list_items:
					if (k.estado == "aprobado"):
						apro = apro + 1
				if(len(list_items)==apro):
					li_b = DBSession.query(LineaBase).filter(LineaBase.id_lb==lb).all()
					for m in li_b:
						m.estado = "cerrado"
						DBSession.merge(m)
					#**************************************************************************************hasta aca
			
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
			historial.cod_recurso = item.cod_item
			historial.tipo_recurso = "Item"
			historial.nombre_recurso = item.nombre_item
			historial.operacion = "Aprobacion"
			historial.fecha_operacion = anho+'-'+mes+'-'+dia
			historial.hora = hora+':'+min+':'+seg
			historial.nombre_usuario = user.user_name
			DBSession.add(historial)
			flash("Item aprobado")
			redirect('/desarrollo/item/list/'+str(self.id_fase))

#~ ************************************************************************************ aca copia todito.. Calculo de Impacto...
	"""Clases utilizadas para generan el calculo de impacto"""
	"""Clases utilizadas para generan el calculo de impacto"""
	def Impacto(self, grafo, item):
		antes_list = list(set(self.IAntecesor(grafo, grafo.incidents(int(item))))) # lista de antecesores
		itemI = [item] 
		despues_list = list(set(self.ISucesor(grafo, grafo.neighbors(int(item))))) #lista de sucesores
		listFinal = antes_list + itemI + despues_list #lista para el costo
		costo = 0;
		for i in listFinal:
			item1 = DBSession.query(Item).get(i)
			costo = costo + item1.complejidad
		return costo, listFinal

	""" Obtine la lista de todos los items aprovados"""
	def getItemsA(self, id_fase):
		iAprobados = DBSession.query(Item).\
		filter(Item.fase==idfase).\
		filter(Item.estado=="aprobado").all()
		return iAprobados

	"""Obtiene padres"""
	def getPadre(self, item):
		relacion = DBSession.query(Relacion).\
		filter(Relacion.id_item2==item.id_item).\
		filter(Relacion.tiporelacion=="Padre Hijo").first()
		
		padre = DBSession.query(Item.id_item)
		
		return padre

	""" Obtine la lista de todos los items antecesores"""
	def IAntecesor (self, grafo, itemsl):
		if(len(itemsl)==0):
			return [] # retorna la lista vacia si no tiene antecesores
		if(len(itemsl)==0 and len(grafo.incidents(itemsl[0]))==0):
			return [items[0]] # retona la lista vacia si  itemsl no tiene antecesores y ademas no existen conflictos en agregar un nodo
		lista = []
		for item in itemsl:
			if (item in lista):
				lista = lista + self.IAntecesor(grafo, grafo.incidents(item))
			else:
				lista = lista + self.IAntecesor(grafo, grafo.incidents(item)) + [item]
		return lista

	""" Obtine la lista de todos los items sucesores"""
	def ISucesor (self, grafo, itemsl):
		if(len(itemsl)==0):
			return [] # retorna la lista vacia si no tiene sucesores
		if(len(itemsl)==0 and len(grafo.neighbors(itemsl[0]))==0):
			return [items[0]] # retona la lista vacia si  itemsl no tiene antecesores y ademas no existen conflictos en agregar un nodo
		lista = []
		for item in itemsl:
			if (item in lista):
				lista = lista + self.ISucesor(grafo, grafo.neighbors(item))
			else:
				lista = lista + self.ISucesor(grafo, grafo.neighbors(item)) + [item]
		return lista
	
	"""Verifica que no se formen ciclos en el grafo."""
	def ciclo (self, id1, id2, idfase):
		grafo = self.GraficoFase(idfase)
		if(grafo.has_edge((id1,id2))):
			return []
			grafo.add_edge((id1,id2))
			return cycle(grafo)
	
	
	"""Grafico dentro de la fase"""
	def GraficoFase(self, id_fase):
		tipos = DBSession.query(TipoItem.id_tipoitem).filter(TipoItem.id_fase==id_fase).all()
		
		itemfase = []
			# todos los items que estan en la fase 
		for j in tipos:
			item = DBSession.query(Item.id_item).filter(Item.id_tipoitem==j.id_tipoitem)
			itemfase.extend(item) 
			
		listitems = []
		grafo = digraph()
		for nodo in itemfase:
			grafo.add_nodes([nodo.id_item])
		
		#~ buscar relaciones de los nodos... (items)
		for nodo in itemfase:
			listitems = listitems + [nodo.id_item] #agrega el id del item a la lista
			
		relaciones = DBSession.query(Relacion).\
		filter(Relacion.tiporelacion=="Padre Hijo").\
		filter(Relacion.id_item1.in_(listitems)).\
		filter(Relacion.id_item2.in_(listitems)).all()
			
		for relacion in relaciones:
			grafo.add_edge((relacion.id_item1,relacion.id_item2))

		return grafo
	""" Realiza el grafico recorriendo por proyecto"""
	#@expose()
	#~ def GraficoProyecto(self, id_proyecto):
		#~ fases = DBSession.query(Fase).filter(Fase.id_proyecto==id_proyecto).all()
		#~ 
		#~ grafo = digraph()
		#~ tipos = []
		#~ items = []
		#~ listitem = []
#~ 
		#~ for i in fases: # todos los items que estan en la fase 
			#~ tipo = DBSession.query(TipoItem.id_tipoitem).filter(TipoItem.id_fase==i.id_fase)
			#~ tipos.extend(tipo)
		#~ for j in tipos:
			#~ item = DBSession.query(Item.id_item).filter(Item.id_tipoitem==j.id_tipoitem)
			#~ items.extend(item) 
#~ 
		#~ for k in items: # por cada item que este en la fase
			#~ grafo.add_nodes([int(k.id_item)])
#~ 
		#~ for l in items: # lista de los ids de items que fueron anadidos
			#~ listitem = listitem + [l.id_item]
#~ # de la lista final de items obtiene las relaciones
		#~ relaciones = DBSession.query(Relacion).\
		#~ filter((Relacion.id_item1).in_(listitem)).all()
#~ 
		#~ for r in relaciones: #agrega la aristas al grafo
			#~ grafo.add_edge((int(r.id_item1), int(r.id_item2)))
#~ 
		#~ return grafo
	def GraficoProyecto(self, id_proyecto):
		fases = DBSession.query(Fase).filter(Fase.id_proyecto==id_proyecto).all()
		
		grafo = digraph()
		tipos = []
		items = []
		listitem = []

		###Aca empieza lo que cambie ######
		colores = ['blue','cyan','green','yellow','orange','purple','gray', 'black']
		indexColor = 0

		for i in fases: # todos los items que estan en la fase 
			tipo = DBSession.query(TipoItem.id_tipoitem).filter(TipoItem.id_fase==i.id_fase)
			#tipos.extend(tipo)

			for j in tipos:
				item = DBSession.query(Item.id_item).filter(Item.id_tipoitem==j.id_tipoitem)
				#items.extend(item) 

				for k in items: # por cada item que este en la fase agregamos los nodos del mismo color

					#Agrego el nodo
					grafo.add_node(int(k.id_item),attrs=[('color', colores[indexColor])])
					
					#Agrego a mi lista grobal de items, para luego sacar las relaciones
					listitem = listitem + [k.id_item]

			# Cambio el color para la siguiente fase			
			if indexColor ==7:
				indexColor = 0
			else:
				indexColor = indexColor + 1
		
		###Aca termina lo que cambie ######

		# de la lista final de items obtiene las relaciones
		relaciones = DBSession.query(Relacion).\
		filter((Relacion.id_item1).in_(listitem)).all()

		for r in relaciones: #agrega la aristas al grafo
			grafo.add_edge((int(r.id_item1), int(r.id_item2)))

		return grafo

		
	@expose('sgs.templates.desarrollo.fase.grafico')
	def CalculoImpacto(self, id_item):
		"""Metodo invocado calcular el impacto"""
		item = DBSession.query(Item).get(id_item)
		fase = item.tipo_item.id_fase
		proy = DBSession.query(Fase.id_proyecto).filter(Fase.id_fase==fase).one()
		grafo = self.GraficoProyecto(proy)
		costoF, listaF = self.Impacto(grafo, id_item)
		
		relaciones = DBSession.query(Relacion).\
		filter((Relacion.id_item1).in_(listaF)).all()
		grafico = self.GraficarGrafo(grafo, proy)
		flash('Calculo de Impacto del item ' +str(id_item) + ' , es '+str(costoF))
		return dict(relaciones=relaciones)
	
	@expose('sgs.templates.desarrollo.fase.grafico')
	def GraficarGrafo(self, grafo, proy):
		grafof = self.GraficoProyecto(proy)
		dot = write(grafof)
		_gvv = _gv.readstring(dot)
		_gv.layout(_gvv,'dot')
		_gv.render(_gvv,'png',"sgs/public/images/grafo.png")
		return dict()
