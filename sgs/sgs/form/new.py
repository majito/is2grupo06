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
from tw.forms.fields import CheckBox
from sprox.dojo.formbase import DojoAddRecordForm


class NewUsuarioForm(DojoAddRecordForm):
	__model__ = Usuario
	__omit_fields__ = ['proyect']
	__field_order__ = ['cod_usuario', 'nombre', 'user_name', '_password', 'password', 'groups']
new_usuario_form = NewUsuarioForm(DBSession)


class NewProyectoForm(DojoAddRecordForm):
	__model__ = Proyecto
	__omit_fields__ = ['fases']
	__field_order__ = ['cod_proyecto', 'nombre_proyecto', 'descripcion', 'fecha_inicio']
new_proyecto_form = NewProyectoForm(DBSession)


class NewRolForm(DojoAddRecordForm):
	__model__ = Rol
	__omit_fields__ = ['users']
	__field_order__ = ['cod_rol', 'group_name', 'descripcion']
new_rol_form = NewRolForm(DBSession)


class NewFaseForm(DojoAddRecordForm):
	__model__ = Fase
new_fase_form = NewFaseForm(DBSession)


class NewTipoItemForm(DojoAddRecordForm):
	__model__ = TipoItem
new_tipoitem_form = NewTipoItemForm(DBSession)


class NewDetalleTipoItemForm(DojoAddRecordForm):
	__model__ = DetalleTipoItem
new_detalletipoitem_form = NewDetalleTipoItemForm(DBSession)


class NewItemForm(DojoAddRecordForm):
	__model__ = Item
new_item_form = NewItemForm(DBSession)


class NewDetalleItemForm(DojoAddRecordForm):
	__model__ = DetalleItem
new_detalleitem_form = NewDetalleItemForm(DBSession)


class NewRelacionForm(DojoAddRecordForm):
	__model__ = Relacion
new_relacion_form = NewRelacionForm(DBSession)


class NewLineaBaseForm(DojoAddRecordForm):
	__model__ = LineaBase
new_lineabase_form = NewLineaBaseForm(DBSession)
