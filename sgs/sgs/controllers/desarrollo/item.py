"""Item Rest Controller Info"""
from datetime import datetime
from tg.controllers import RestController, redirect
from tg.decorators import expose, validate, with_trailing_slash
from sgs.model import DBSession
from sgs.model.model import *
from tg import tmpl_context
from sgs.form.new import *
from sgs.form.list import *


#from sprox.formbase import AddRecordForm

#__all__ = ['ItemRestController']

class ItemRestController(RestController):


    @expose('sgs.templates.desarrollo.item.new')
    def new(self, **kw):
        tmpl_context.widget = new_item_form
        return dict(value=kw)


    @validate(new_item_form, error_handler=new)
    @expose()
    def post(self, _method='', **kw):
        del kw['sprox_id']
        item = Item(**kw)
        DBSession.add(item)
        flash('Item creado')
        redirect('/desarrollo/item/list')


    @expose('sgs.templates.desarrollo.item.list')
    def list(self):
        tmpl_context.widget = list_item
        value = list_item_filler.get_value()
        return dict(value=value)



