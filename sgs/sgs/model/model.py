# -*- coding: utf-8 -*-

import os
from datetime import datetime
import sys

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref, synonym
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym
from sgs.model import DeclarativeBase, metadata, DBSession



try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')


__all__ = ['Usuario', 'Rol', 'Permiso', 'Proyecto','Fase','TipoItem','Item','LineaBase','Relacion','VersionadoItem','ArchivosExternos','Historico','DetalleTipoItem','DetalleItem','DetalleVersionadoItem']


#{ Tablas de asociaciones

# Tabla de asociacion muchos a muchos entre Usuarios y Roles
rol_por_usuario_tabla = Table('rol_por_usuario', metadata,
    Column('id_rol', Integer, ForeignKey('rol.id_rol',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion muchos a muchos entre permisos y roles
permiso_por_rol_tabla = Table('permiso_por_rol', metadata,
    Column('id_permiso', Integer, ForeignKey('permiso.id_permiso',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_rol', Integer, ForeignKey('rol.id_rol',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion muchos a muchos entre Usuarios y Proyectos
usuario_por_proyecto_tabla = Table('usuario_por_proyecto', metadata,
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_proyecto', Integer, ForeignKey('proyecto.id_proyecto',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion muchos a muchos entre Usuarios y Proyectos
usuario_por_fase_tabla = Table('usuario_por_fase', metadata,
    Column('id_usuario', Integer, ForeignKey('usuario.id_usuario',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_fase', Integer, ForeignKey('fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE"))
)



# Tabla de asociacion muchos a uno entre Lineas Base y Fases
linea_base_por_fase_tabla = Table('linea_base_por_fase', metadata,
    Column('id_lb', Integer, ForeignKey('linea_base.id_lb',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_fase', Integer, ForeignKey('fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE"))
)


# Tabla de asociacion muchos a uno entre fases y proyectos
fase_por_proyecto_tabla = Table('fase_por_proyecto', metadata,
    Column('id_fase', Integer, ForeignKey('fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_proyecto', Integer, ForeignKey('proyecto.id_proyecto',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion muchos a uno entre items y Lineas Base
item_por_linea_base_tabla = Table('item_por_linea_base', metadata,
    Column('id_item', Integer, ForeignKey('item.id_item',
        onupdate="CASCADE", ondelete="CASCADE")),

     Column('id_lb', Integer, ForeignKey('linea_base.id_lb',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion muchos a muchos entre tipo de items y fases
tipo_item_por_fase_tabla = Table('tipo_item_por_fase', metadata,
    Column('id_tipoitem', Integer, ForeignKey('tipo_item.id_tipoitem',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_fase', Integer, ForeignKey('fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion uno a muchos entre relaciones e items
relacion_por_item_tabla = Table('relacion_por_item', metadata,
    Column('id_relacion', Integer, ForeignKey('relacion.id_relacion',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_item', Integer, ForeignKey('item.id_item',
        onupdate="CASCADE", ondelete="CASCADE"))
)

# Tabla de asociacion muchos a muchos entre permisos, roles y fases
permiso_por_rol_por_fase_tabla = Table('permiso_por_rol_por_fase', metadata,
    Column('id_permiso', Integer, ForeignKey('permiso.id_permiso',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_fase', Integer, ForeignKey('fase.id_fase',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_rol', Integer, ForeignKey('rol.id_rol',
        onupdate="CASCADE", ondelete="CASCADE"))
)


detalle_por_tipo_item_tabla = Table('detalle_por_tipo_item_tabla', metadata,
    Column('id_tipoitem', Integer, ForeignKey('tipo_item.id_tipoitem',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_detalletipoitem', Integer, ForeignKey('detalle_tipo_item.id_detalletipoitem',
        onupdate="CASCADE", ondelete="CASCADE"))
)


detalle_por_item_tabla = Table('detalle_por_item_tabla', metadata,
    Column('id_item', Integer, ForeignKey('item.id_item',
        onupdate="CASCADE", ondelete="CASCADE")),
    Column('id_detalleitem', Integer, ForeignKey('detalle_item.id_detalleitem',
        onupdate="CASCADE", ondelete="CASCADE"))
)




class Rol(DeclarativeBase):
    """
    Group definition for :mod:`repoze.what`.
    
    Only the ``group_name`` column is required by :mod:`repoze.what`.
    
    """
    
    __tablename__ = 'rol'
    
    #{ Columns
    
    id_rol = Column(Integer, autoincrement=True, primary_key=True)

    cod_rol = Column(Unicode(10), unique=True, nullable=False)

    group_name = Column(Unicode(20), unique=True, nullable=False)

    descripcion = Column(Unicode(255))

#    created = Column(DateTime, default=datetime.now)

    #{ Relations

    users = relation('Usuario', secondary=rol_por_usuario_tabla, backref='groups')

   
    #{ Special methods
    
    def __repr__(self):
        return '<Rol: name=%s>' % self.group_name
    
    def __unicode__(self):
        return self.group_name
    
    #}


class Usuario(DeclarativeBase):
    """
    User definition.
    
    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.
    
    """
    __tablename__ = 'usuario'
    
    #{ Columns

    id_usuario = Column(Integer, autoincrement=True, primary_key=True)

    cod_usuario = Column(Unicode(20), unique=True, nullable=False)
    
    user_name = Column(Unicode(20), unique=True, nullable=False)
    
#    email_address = Column(Unicode(255), unique=True, nullable=False,
#                           info={'rum': {'field':'Email'}})
    
    nombre = Column(Unicode(20))
    
    _password = Column('password', Unicode(80),
                       info={'rum': {'field':'Password'}})
    
#    created = Column(DateTime, default=datetime.now)
    
    #{ Special methods

    def __repr__(self):
        return '<Usuario: display name="%s">' % (
                self.nombre)

    def __unicode__(self):
        return self.user_name
    
    #{ Getters and setters

    @property
    def permissions(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

#    @classmethod
#    def by_email_address(cls, email):
#        """Return the user object whose email address is ``email``."""
#        return DBSession.query(cls).filter(cls.email_address==email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter(cls.user_name==username).first()

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        hashed_password = password
        
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        # Make sure the hashed password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode
        # columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))
    
    #}
    
    def validate_password(self, password):
        """
        Check the password against existing credentials.
        
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()


class Permiso(DeclarativeBase):
    """
    Permission definition for :mod:`repoze.what`.
    
    Only the ``permission_name`` column is required by :mod:`repoze.what`.
    
    """
    
    __tablename__ = 'permiso'


    id_permiso = Column(Integer, autoincrement=True, primary_key=True)

    cod_permiso = Column(Unicode(10), unique=True, nullable=False)

    permission_name = Column(Unicode(20), nullable=False)

    descripcion = Column(Unicode(100))

    #{ Relations

    groups = relation(Rol, secondary=permiso_por_rol_tabla, 
                      backref='permissions')   

    #{ Special methods
    
    def __repr__(self):
        return '<Permiso: name=%s>' % self.permission_name

    def __unicode__(self):
        return self.permission_name
    
    #}




class Proyecto(DeclarativeBase):
    __tablename__ = 'proyecto'
    
    #{ Columns
    
    id_proyecto = Column(Integer, autoincrement=True, primary_key=True)
      
    cod_proyecto = Column(Unicode(10), unique=True, nullable=False)

    nombre_proyecto = Column(Unicode(20), nullable=False)
    
    descripcion = Column(Unicode(100))

    fecha_inicio = Column(Date) ########################################################

    #{ Relations ################################

    usuarios = relation('Usuario', secondary=usuario_por_proyecto_tabla, backref='proyect')
    
    #}


class Fase(DeclarativeBase):
    __tablename__ = 'fase'
    
    #{ Columns
    
    id_fase = Column(Integer, autoincrement=True, primary_key=True)

    cod_fase = Column(Unicode(10), unique=True, nullable=False)

    nombre_fase = Column(Unicode(20), nullable=False)
    
    descripcion = Column(Unicode(255))
 
    #{ Relations ##########################
    
    participantes = relation('Usuario', secondary=usuario_por_fase_tabla)#, backref='fasesparticipantes')

    proyectos = relation('Proyecto', secondary=fase_por_proyecto_tabla, backref='fases')

    #}



class TipoItem(DeclarativeBase):
    __tablename__ = 'tipo_item'
    
    #{ Columns
    
    id_tipoitem = Column(Integer, autoincrement=True, primary_key=True)
    
    cod_tipoitem = Column(Unicode(10), unique=True, nullable=False)
    
    nombre_tipoitem = Column(Unicode(20), nullable=False)
    
    descripcion = Column(Unicode(100))

    fase = Column(Unicode(10), nullable=False)

#    detallestipo = relation('DetalleTipoItem', secondary=detalle_por_tipo_item_tabla, backref='tipos')
    
    #}


class Item(DeclarativeBase):
    __tablename__ = 'item'
    
    #{ Columns
    
    id_item = Column(Integer, autoincrement=True, primary_key=True)

    cod_item = Column(Unicode(10), unique=True, nullable=False)
    
    nombre_item = Column(Unicode(20), nullable=False)
    
    descripcion = Column(Unicode(100))

    version = Column(Integer, nullable=False)

    estado = Column(Unicode(10), nullable=False)

    complejidad = Column(Integer, nullable=False)

#    detallesitem = relation('DetalleItem', secondary=detalle_por_item_tabla, backref='items')
    
    #}



class LineaBase(DeclarativeBase):
    __tablename__ = 'linea_base'
    
    #{ Columns
    
    id_lb = Column(Integer, autoincrement=True, primary_key=True)

    cod_lb = Column(Unicode(10), unique=True, nullable=False)
    
    fase = Column(Unicode(10), nullable=False)
    
    estado = Column(Unicode(10), nullable=False)

    #}



class Relacion(DeclarativeBase):
    __tablename__ = 'relacion'
    
    #{ Columns
    
    id_relacion = Column(Integer, autoincrement=True, primary_key=True)

    cod_relacion = Column(Unicode(10), unique=True, nullable=False)
    
    descripcion = Column(Unicode(100))

    tiporelacion = Column(Unicode(10), nullable=False)

    #}


class VersionadoItem(DeclarativeBase):
    __tablename__ = 'versionado_item'
    
    #{ Columns
    
    id_versionado = Column(Integer, autoincrement=True, primary_key=True)

    cod_item = Column(Unicode(10), unique=True, nullable=False)
    
    nombre_item = Column(Unicode(40), nullable=False)

    descripcion = Column(Unicode(100))

    version = Column(Integer, nullable=False)

    complejidad = Column(Integer, nullable=False)

    #}



class ArchivosExternos(DeclarativeBase):
    __tablename__ = 'archivos_externos'
    
    #{ Columns
    
    id_arcesterno = Column(Integer, autoincrement=True, primary_key=True)

    id_item = Column(Integer, unique=True, nullable=False)
    
    tipo_archivo = Column(Integer, nullable=False)

    descripcion = Column(Unicode(100))

    archivo = Column(Unicode(10))

    #}



class Historico(DeclarativeBase):
    __tablename__ = 'historico'
    
    #{ Columns
    
    id_historico = Column(Integer, autoincrement=True, primary_key=True)

    id_recurso = Column(Integer, unique=True, nullable=False)
    
    nombre_recurso = Column(Unicode(20), nullable=False)

    operacion = Column(Unicode(50))

    fecha_operacion = Column(Date, nullable=False)

    hora = Column(Time, nullable=False)

    nombre_usuario = Column(Unicode(20), nullable=False)

    #}


class DetalleTipoItem(DeclarativeBase):
    __tablename__ = 'detalle_tipo_item'
    
    #{ Columns
    
    id_detalletipoitem = Column(Integer, autoincrement=True, primary_key=True)

#    id_tipoitem = Column(Integer, ForeignKey('tipo_item.id_tipoitem')) ##hay que sacar y hacer con relation
    
    nombre_atributo = Column(Unicode(100), nullable=False)

    tipo_dato = Column(Unicode(60), nullable=False)

    tipositem = relation('TipoItem', secondary=detalle_por_tipo_item_tabla, backref='detallestipo')
    
    #}

class DetalleItem(DeclarativeBase):
    __tablename__ = 'detalle_item'
    
    #{ Columns
    
    id_detalleitem = Column(Integer, autoincrement=True, primary_key=True)
 
#    id_item = Column(Integer, ForeignKey('item.id_item')) ##hay que sacar y hacer con relation
    
    nombre_atributo = Column(Unicode(100), nullable=False)

    tipo_dato = Column(Unicode(60), nullable=False)

    valor = Column(Unicode(100), nullable=False)

    items = relation('Item', secondary=detalle_por_item_tabla, backref='detallesitem')

    
    #}


class DetalleVersionadoItem(DeclarativeBase):
    __tablename__ = 'detalle_versionado_item'
    
    #{ Columns
    
    id_detalleversionitem = Column(Integer, autoincrement=True, primary_key=True)

    id_versionado = Column(Integer, ForeignKey('versionado_item.id_versionado'))
    
    nombre_atributo = Column(Unicode(100), nullable=False)

    tipo_dato = Column(Unicode(60), nullable=False)

    valor = Column(Unicode(100), nullable=False)

    
    #}









