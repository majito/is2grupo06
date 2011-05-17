"""Edit"""
from datetime import datetime
from tg.controllers import RestController, redirect
from pylons import request
from tg.decorators import expose, validate, with_trailing_slash
from sgs.model import DBSession
from sgs.model.model import *
from formencode.validators import DateConverter, Int, NotEmpty
from sprox.formbase import EditableForm
from sprox.fillerbase import EditFormFiller

from sprox.formbase import AddRecordForm


#USUARIO
class EditUsuarioForm(EditableForm):
    __model__ = Usuario
edit_usuario_form = EditUsuarioForm(DBSession)

class EditUsuarioFiller(EditFormFiller):
    __model__ = Usuario
edit_usuario_filler = EditUsuarioFiller(DBSession)


#PROYECTO
class EditProyectoForm(EditableForm):
    __model__ = Proyecto
edit_proyecto_form = EditProyectoForm(DBSession)

class EditProyectoFiller(EditFormFiller):
    __model__ = Proyecto
edit_proyecto_filler = EditProyectoFiller(DBSession)


#ROL
class EditRolForm(EditableForm):
    __model__ = Rol
edit_rol_form = EditRolForm(DBSession)

class EditRolFiller(EditFormFiller):
    __model__ = Rol
edit_rol_filler = EditRolFiller(DBSession)


#FASE
class EditFaseForm(EditableForm):
    __model__ = Fase
edit_fase_form = EditFaseForm(DBSession)

class EditFaseFiller(EditFormFiller):
    __model__ = Fase
edit_fase_filler = EditFaseFiller(DBSession)


#TIPO DE ITEM
class EditTipoItemForm(EditableForm):
    __model__ = TipoItem
edit_tipoitem_form = EditTipoItemForm(DBSession)

class EditTipoItemFiller(EditFormFiller):
    __model__ = TipoItem
edit_tipoitem_filler = EditTipoItemFiller(DBSession)


#DETALLE TIPO DE ITEM
class EditDetalleTipoItemForm(EditableForm):
    __model__ = DetalleTipoItem
edit_detalletipoitem_form = EditDetalleTipoItemForm(DBSession)

class EditDetalleTipoItemFiller(EditFormFiller):
    __model__ = DetalleTipoItem
edit_detalletipoitem_filler = EditDetalleTipoItemFiller(DBSession)


#ITEM
class EditItemForm(EditableForm):
    __model__ = Item
edit_item_form = EditItemForm(DBSession)

class EditItemFiller(EditFormFiller):
    __model__ = Item
edit_item_filler = EditItemFiller(DBSession)


#DETALLE DE ITEM
class EditDetalleItemForm(EditableForm):
    __model__ = DetalleItem
edit_detalleitem_form = EditDetalleItemForm(DBSession)

class EditDetalleItemFiller(EditFormFiller):
    __model__ = DetalleItem
edit_detalleitem_filler = EditDetalleItemFiller(DBSession)

#RELACION
class EditRelacionForm(EditableForm):
    __model__ = Relacion
edit_relacion_form = EditRelacionForm(DBSession)

class EditRelacionFiller(EditFormFiller):
    __model__ = Relacion
edit_relacion_filler = EditRelacionFiller(DBSession)

