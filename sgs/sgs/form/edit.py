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
from sprox.dojo.formbase import DojoEditableForm


#USUARIO
class EditUsuarioForm(DojoEditableForm):
	__model__ = Usuario
	__omit_fields__ = ['cod_usuario', 'proyect']
	__field_order__ = ['nombre', 'user_name', '_password', 'password', 'groups']
edit_usuario_form = EditUsuarioForm(DBSession)

class EditUsuarioFiller(EditFormFiller):
	__model__ = Usuario
edit_usuario_filler = EditUsuarioFiller(DBSession)


#PROYECTO
class EditProyectoForm(DojoEditableForm):
    __model__ = Proyecto
    __omit_fields__ = ['cod_proyecto', 'fases']
edit_proyecto_form = EditProyectoForm(DBSession)

class EditProyectoFiller(EditFormFiller):
    __model__ = Proyecto
edit_proyecto_filler = EditProyectoFiller(DBSession)


#ROL
class EditRolForm(DojoEditableForm):
    __model__ = Rol
    __omit_fields__ = ['users', 'cod_rol']
edit_rol_form = EditRolForm(DBSession)

class EditRolFiller(EditFormFiller):
    __model__ = Rol
edit_rol_filler = EditRolFiller(DBSession)


#FASE
class EditFaseForm(DojoEditableForm):
    __model__ = Fase
    __omit_fields__ = ['cod_fase']
edit_fase_form = EditFaseForm(DBSession)

class EditFaseFiller(EditFormFiller):
    __model__ = Fase
edit_fase_filler = EditFaseFiller(DBSession)


#TIPO DE ITEM
class EditTipoItemForm(DojoEditableForm):
    __model__ = TipoItem
    __omit_fields__ = ['cod_tipoitem']
edit_tipoitem_form = EditTipoItemForm(DBSession)

class EditTipoItemFiller(EditFormFiller):
    __model__ = TipoItem
edit_tipoitem_filler = EditTipoItemFiller(DBSession)


#DETALLE TIPO DE ITEM
class EditDetalleTipoItemForm(DojoEditableForm):
    __model__ = DetalleTipoItem
    __omit_fields__ = ['cod_detalletipoitem']
edit_detalletipoitem_form = EditDetalleTipoItemForm(DBSession)

class EditDetalleTipoItemFiller(EditFormFiller):
    __model__ = DetalleTipoItem
edit_detalletipoitem_filler = EditDetalleTipoItemFiller(DBSession)


#ITEM
class EditItemForm(DojoEditableForm):
    __model__ = Item
    __omit_fields__ = ['cod_item']
edit_item_form = EditItemForm(DBSession)

class EditItemFiller(EditFormFiller):
    __model__ = Item
edit_item_filler = EditItemFiller(DBSession)


#DETALLE DE ITEM
class EditDetalleItemForm(DojoEditableForm):
    __model__ = DetalleItem
    __omit_fields__ = ['cod_detalleitem']
edit_detalleitem_form = EditDetalleItemForm(DBSession)

class EditDetalleItemFiller(EditFormFiller):
    __model__ = DetalleItem
edit_detalleitem_filler = EditDetalleItemFiller(DBSession)

#RELACION
class EditRelacionForm(DojoEditableForm):
    __model__ = Relacion
    __omit_fields__ = ['cod_relacion']
edit_relacion_form = EditRelacionForm(DBSession)

class EditRelacionFiller(EditFormFiller):
    __model__ = Relacion
edit_relacion_filler = EditRelacionFiller(DBSession)

