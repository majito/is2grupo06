"""New"""
import pylons
from datetime import datetime
from tg.controllers import RestController, redirect
from pylons import request
from tg.decorators import expose, validate, with_trailing_slash
from sgs.model import DBSession
from sgs.model.model import *
from formencode.validators import DateConverter, Int, NotEmpty
from sprox.tablebase import TableBase
from sprox.formbase import AddRecordForm

class NewUsuarioForm(AddRecordForm):
    __model__ = Usuario
new_usuario_form = NewUsuarioForm(DBSession)


class NewProyectoForm(AddRecordForm):
    __model__ = Proyecto
new_proyecto_form = NewProyectoForm(DBSession)


class NewRolForm(AddRecordForm):
    __model__ = Rol
new_rol_form = NewRolForm(DBSession)


class NewFaseForm(AddRecordForm):
    __model__ = Fase
new_fase_form = NewFaseForm(DBSession)


class NewTipoItemForm(AddRecordForm):
    __model__ = TipoItem
new_tipoitem_form = NewTipoItemForm(DBSession)


class NewDetalleTipoItemForm(AddRecordForm):
    __model__ = DetalleTipoItem
new_detalletipoitem_form = NewDetalleTipoItemForm(DBSession)


class NewItemForm(AddRecordForm):
    __model__ = Item
new_item_form = NewItemForm(DBSession)


class NewDetalleItemForm(AddRecordForm):
    __model__ = DetalleItem
new_detalleitem_form = NewDetalleItemForm(DBSession)


class NewRelacionForm(AddRecordForm):
    __model__ = Relacion
new_relacion_form = NewRelacionForm(DBSession)


class NewLineaBaseForm(AddRecordForm):
    __model__ = LineaBase
new_lineabase_form = NewLineaBaseForm(DBSession)
