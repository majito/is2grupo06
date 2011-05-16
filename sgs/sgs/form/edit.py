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

class EditUsuarioForm(EditableForm):
    __model__ = Usuario
#    __omit_fields__ = ['genre_id', 'movie_id']
edit_usuario_form = EditUsuarioForm(DBSession)

class EditUsuarioFiller(EditFormFiller):
    __model__ = Usuario
edit_usuario_filler = EditUsuarioFiller(DBSession)
