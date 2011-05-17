"""Listar"""
import pylons
from datetime import datetime
from tg.controllers import RestController, redirect
from pylons import request
from tg.decorators import expose, validate, with_trailing_slash
from sgs.model import DBSession
from sgs.model.model import *
from formencode.validators import DateConverter, Int, NotEmpty

from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm

#USUARIO
class ListUsuario(TableBase):
    __model__ = Usuario
list_usuario = ListUsuario(DBSession)

class ListUsuarioFiller(TableFiller):
    __model__ = Usuario
list_usuario_filler = ListUsuarioFiller(DBSession)


#PROYECTO
class ListProyecto(TableBase):
    __model__ = Proyecto
list_proyecto = ListProyecto(DBSession)

class ListProyectoFiller(TableFiller):
    __model__ = Proyecto
list_proyecto_filler = ListProyectoFiller(DBSession)


#ROL
class ListRol(TableBase):
    __model__ = Rol
list_rol = ListRol(DBSession)

class ListRolFiller(TableFiller):
    __model__ = Rol
list_rol_filler = ListRolFiller(DBSession)


#FASE
class ListFase(TableBase):
    __model__ = Fase
list_fase = ListFase(DBSession)

class ListFaseFiller(TableFiller):
    __model__ = Fase
list_fase_filler = ListFaseFiller(DBSession)


#TIPO DE ITEM
class ListTipoItem(TableBase):
    __model__ = TipoItem
list_tipoitem = ListTipoItem(DBSession)

class ListTipoItemFiller(TableFiller):
    __model__ = TipoItem
list_tipoitem_filler = ListTipoItemFiller(DBSession)


#DETALLE TIPO DE ITEM
class ListDetalleTipoItem(TableBase):
    __model__ = DetalleTipoItem
list_detalletipoitem = ListDetalleTipoItem(DBSession)

class ListDetalleTipoItemFiller(TableFiller):
    __model__ = DetalleTipoItem
list_detalletipoitem_filler = ListDetalleTipoItemFiller(DBSession)


#ITEM
class ListItem(TableBase):
    __model__ = Item
list_item = ListItem(DBSession)

class ListItemFiller(TableFiller):
    __model__ = Item
list_item_filler = ListItemFiller(DBSession)


#DETALLE ITEM
class ListDetalleItem(TableBase):
    __model__ = DetalleItem
list_detalleitem = ListDetalleItem(DBSession)

class ListDetalleItemFiller(TableFiller):
    __model__ = DetalleItem
list_detalleitem_filler = ListDetalleItemFiller(DBSession)


#RELACION
class ListRelacion(TableBase):
    __model__ = Relacion
list_relacion = ListRelacion(DBSession)

class ListRelacionFiller(TableFiller):
    __model__ = Relacion
list_relacion_filler = ListRelacionFiller(DBSession)

#LINEA BASE
class ListLineaBase(TableBase):
    __model__ = LineaBase
list_lineabase = ListLineaBase(DBSession)

class ListLineaBaseFiller(TableFiller):
    __model__ = LineaBase
list_lineabase_filler = ListLineaBaseFiller(DBSession)
