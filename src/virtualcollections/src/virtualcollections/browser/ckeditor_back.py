from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.textfield.widget import RichTextWidget
from virtualcollections.interfaces import ILayer
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


@adapter(getSpecification(IRichText['text']), ILayer)
@implementer(IFieldWidget)
def RichTextFieldWidget(field, request):
    return FieldWidget(field, RichTextWidget(request))
