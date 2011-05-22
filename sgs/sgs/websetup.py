# -*- coding: utf-8 -*-
"""Setup the sgs application"""

import logging

import transaction
from tg import config

from sgs.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):
    """Place any commands to setup sgs here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from sgs import model
    from sgs.model.model import *

    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)


#####USUARIOS#####
    admin = model.Usuario()
    admin.cod_usuario = u'1'
    admin.user_name = u'admin'
    admin.password = u'adminpass'
    admin.nombre = u'Example manager'

    lid = model.Usuario()
    lid.cod_usuario = u'2'
    lid.user_name = u'lider'
    lid.password = u'liderpass'
    lid.nombre = u'Lider de Proyecto'

    part = model.Usuario()
    part.cod_usuario = u'3'
    part.user_name = u'participante'
    part.password = u'participantepass'
    part.nombre = u'Participante Proy'




#####ROLES#####
    administrador = model.Rol()
    administrador.cod_rol = u'1'
    administrador.group_name = u'administradores'
    administrador.descripcion = u'Grupo de Administradores'

    lider = model.Rol()
    lider.cod_rol = u'2'
    lider.group_name = u'lider'
    lider.descripcion = u'Rol de lider de proyecto'

    participante = model.Rol()
    participante.cod_rol = u'3'
    participante.group_name = u'participante'
    participante.descripcion = u'Rol de participante de proyecto'

#####PERMISOS#####
    permiso1 = model.Permiso()
    permiso1.cod_permiso = u'1'
    permiso1.permission_name = u'ver_usuario_todos'
    permiso1.descripcion = u'Permiso para ver usuario'

    permiso2 = model.Permiso()
    permiso2.cod_permiso = u'2'
    permiso2.permission_name = u'crear_usuario'
    permiso2.descripcion = u'Permiso para crear usuario'

    permiso3 = model.Permiso()
    permiso3.cod_permiso = u'3'
    permiso3.permission_name = u'editar_usuario'
    permiso3.descripcion = u'Permiso para editar usuario'

    permiso4 = model.Permiso()
    permiso4.cod_permiso = u'4'
    permiso4.permission_name = u'eliminar_usuario'
    permiso4.descripcion = u'Permiso para eliminar usuario'

    permiso5 = model.Permiso()
    permiso5.cod_permiso = u'5'
    permiso5.permission_name = u'ver_proyecto_todos'
    permiso5.descripcion = u'Permiso para ver proyecto'

    permiso6 = model.Permiso()
    permiso6.cod_permiso = u'6'
    permiso6.permission_name = u'crear_proyecto'
    permiso6.descripcion = u'Permiso para crear proyecto'

    permiso7 = model.Permiso()
    permiso7.cod_permiso = u'7'
    permiso7.permission_name = u'editar_proyecto'
    permiso7.descripcion = u'Permiso para editar proyecto'

    permiso8 = model.Permiso()
    permiso8.cod_permiso = u'8'
    permiso8.permission_name = u'eliminar_proyecto'
    permiso8.descripcion = u'Permiso para eliminar proyecto'

#    permiso9 = model.Permiso()
#    permiso9.cod_permiso = u'9
#    permiso9.nombre_permiso = u'asignar_usuario_proyecto'
#    permiso9.descripcion = u'Permiso para asignar un usuario a un proyecto'

#    permiso10= model.Permiso()
#    permiso10.cod_permiso = u'10'
#    permiso10.nombre_permiso = u'ver_rol_todos'
#    permiso10.descripcion = u'Permiso para ver rol'

#    permiso11= model.Permiso()
#    permiso11.cod_permiso = u'11'
#    permiso11.permission_name = u'crear_rol'
#    permiso11.descripcion = u'Permiso para crear rol'

#    permiso12= model.Permiso()
#    permiso12.cod_permiso = u'12'
#    permiso12.permission_name = u'editar_rol'
#    permiso12.descripcion = u'Permiso para editar rol'

#    permiso13= model.Permiso()
#    permiso13.cod_permiso = u'13'
#    permiso13.permission_name = u'eliminar_rol'
#    permiso13.descripcion = u'Permiso para eliminar rol'

#    permiso14= model.Permiso()
#    permiso14.cod_permiso = u'14'
#    permiso14.permission_name = u'asignar_rol_admin'
#    permiso14.descripcion = u'Permiso para que un administrador asigne el rol de admin o de lider'

#    permiso15= model.Permiso()
#    permiso15.cod_permiso = u'15'
#    permiso15.permission_name = u'asignar_rol_lider'
#    permiso15.descripcion = u'Permiso para que un lider asigne un rol a participantes de su proyecto'


#    permiso16= model.Permiso()
#    permiso16.cod_permiso = u'16'
#    permiso16.permission_name = u'ver_fase_todos'
#    permiso16.descripcion = u'Permiso para ver todas las fases'

#    permiso17= model.Permiso()
#    permiso17.cod_permiso = u'17'
#    permiso17.permission_name = u'crear_fase'
#    permiso17.descripcion = u'Permiso para crear fases'

#    permiso18= model.Permiso()
#    permiso18.cod_permiso = u'18'
#    permiso18.permission_name = u'editar_fase'
#    permiso18.descripcion = u'Permiso para editar fases'

#    permiso19= model.Permiso()
#    permiso19.cod_permiso = u'19'
#    permiso19.permission_name = u'eliminar_fase'
#    permiso19.descripcion = u'Permiso para eliminar fases'

#    permiso20= model.Permiso()
#    permiso20.cod_permiso = u'20'
#    permiso20.permission_name = u'ver_tipoitem_todos'
#    permiso20.descripcion = u'Permiso para ver todos los tipos de items'

#    permiso21= model.Permiso()
#    permiso21.cod_permiso = u'21'
#    permiso21.permission_name = u'crear_tipoitem'
#    permiso21.descripcion = u'Permiso para crear tipo de item'

#    permiso22= model.Permiso()
#    permiso22.cod_permiso = u'22'
#    permiso22.permission_name = u'editar_tipoitem'
#    permiso22.descripcion = u'Permiso para editar tipo de item'

#    permiso23= model.Permiso()
#    permiso23.cod_permiso = u'23'
#    permiso23.permission_name = u'eliminar_tipoitem'
#    permiso23.descripcion = u'Permiso para eliminar tipo de item'

#    permiso24= model.Permiso()
#    permiso24.cod_permiso = u'24'
#    permiso24.permission_name = u'ver_item_todos'
#    permiso24.descripcion = u'Permiso para ver todos los items'

#    permiso25= model.Permiso()
#    permiso25.cod_permiso = u'25'
#    permiso25.permission_name = u'crear_item'
#    permiso25.descripcion = u'Permiso para crear item'

#    permiso26= model.Permiso()
#    permiso26.cod_permiso = u'26'
#    permiso26.permission_name = u'editar_item'
#    permiso26.descripcion = u'Permiso para editar item'

#    permiso27= model.Permiso()
#    permiso27.cod_permiso = u'27'
#    permiso27.permission_name = u'eliminar_item'
#    permiso27.descripcion = u'Permiso para eliminar item'

#    permiso28= model.Permiso()
#    permiso28.cod_permiso = u'28'
#    permiso28.permission_name = u'ver_relacion_todos'
#    permiso28.descripcion = u'Permiso para ver todas las relaciones'

#    permiso29= model.Permiso()
#    permiso29.cod_permiso = u'29'
#    permiso29.permission_name = u'crear_relacion'
#    permiso29.descripcion = u'Permiso para crear relacion'

#    permiso30= model.Permiso()
#    permiso30.cod_permiso = u'30'
#    permiso30.permission_name = u'editar_relacion'
#    permiso30.descripcion = u'Permiso para editar relacion'

#    permiso31= model.Permiso()
#    permiso31.cod_permiso = u'31'
#    permiso31.permission_name = u'eliminar_relacion'
#    permiso31.descripcion = u'Permiso para eliminar relacion'

#    permiso32= model.Permiso()
#    permiso32.cod_permiso = u'32'
#    permiso32.permission_name = u'ver_lineabase'
#    permiso32.descripcion = u'Permiso para ver las lineas base'

#    permiso33= model.Permiso()
#    permiso33.cod_permiso = u'33'
#    permiso33.permission_name = u'abrir_lineabase'
#    permiso33.descripcion = u'Permiso para abrir lineas base'

#    permiso34= model.Permiso()
#    permiso34.cod_permiso = u'34'
#    permiso34.permission_name = u'cerrar_lineabase'
#    permiso34.descripcion = u'Permiso para cerrar lineas base'


################### ADMINISTRADOR ################################
    model.DBSession.add(admin)			#USUARIO AL MODELO
    administrador.users.append(admin) 		#ROL AL USUARIO
    model.DBSession.add(administrador)		#ROL AL MODELO
  
    permiso1.groups.append(administrador)	#PERMISO AL ROL
    model.DBSession.add(permiso1)		#PERMISO AL MODELO

    permiso2.groups.append(administrador) 	
    model.DBSession.add(permiso2)		

    permiso3.groups.append(administrador) 	
    model.DBSession.add(permiso3)		

    permiso4.groups.append(administrador) 	
    model.DBSession.add(permiso4)		

    permiso5.groups.append(administrador) 	
    model.DBSession.add(permiso5)		

    permiso6.groups.append(administrador) 	
    model.DBSession.add(permiso6)		

    permiso8.groups.append(administrador) 	
    model.DBSession.add(permiso8)		


################### LIDER DE PROY ################################
    model.DBSession.add(lid)			#USUARIO AL MODELO
    lider.users.append(lid)			#ROL AL USUARIO
    model.DBSession.add(lider)			#ROL AL MODELO

    permiso5.groups.append(lider) 		#PERMISO AL ROL
    model.DBSession.add(permiso5)		#PERMISO AL MODELO

    permiso7.groups.append(lider) 		
    model.DBSession.add(permiso7)		


################### PARTICIPANTE #################################
    model.DBSession.add(part)			#USUARIO AL MODELO
    participante.users.append(part)		#ROL AL USUARIO
    model.DBSession.add(participante)		#ROL AL MODELO
	

#    permiso3.groups.append(administrador) 	#PERMISO AL ROL
#    model.DBSession.add(permiso3)		#PERMISO AL MODELO

#    permiso4.groups.append(administrador) 	
#    model.DBSession.add(permiso4)		

#    permiso5.groups.append(administrador) 	
#    model.DBSession.add(permiso5)		

#    permiso6.groups.append(administrador) 	
#    model.DBSession.add(permiso6)		

##################################################################################

#    lider_proyecto = model.Usuario()
#    lider_proyecto.user_name = u'lider'
#    lider_proyecto.display_name = u'Example editor'
#    lider_proyecto.email_address = u'editor@somedomain.com'
#    lider_proyecto.password = u'liderpass'


#    model.DBSession.add(lider_proyecto)
#    model.DBSession.flush()

#    transaction.commit()
#    print "Successfully setup"


#    manager = model.User()
#    manager.user_name = u'manager'
#    manager.display_name = u'Example manager'
#    manager.email_address = u'manager@somedomain.com'
#    manager.password = u'managepass'

#    model.DBSession.add(manager)

#    group = model.Group()
#    group.group_name = u'managers'
#    group.display_name = u'Managers Group'

#    group.users.append(manager)

#    model.DBSession.add(group)

#    permission = model.Permission()
#    permission.permission_name = u'manage'
#    permission.description = u'This permission give an administrative right to the bearer'
#    permission.groups.append(group)

#    model.DBSession.add(permission)

#    editor = model.User()
#    editor.user_name = u'editor'
#    editor.display_name = u'Example editor'
#    editor.email_address = u'editor@somedomain.com'
#    editor.password = u'editpass'

 #   model.DBSession.add(editor)
    model.DBSession.flush()

    transaction.commit()
    print "Successfully setup"
