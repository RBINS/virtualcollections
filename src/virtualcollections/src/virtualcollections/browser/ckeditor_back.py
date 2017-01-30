from Acquisition import ImplicitAcquisitionWrapper
from UserDict import UserDict

from zope.interface import implementsOnly, implementer
from zope.component import adapts, adapter

from z3c.form.interfaces import ITextAreaWidget, IFieldWidget, NOVALUE
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.browser.widget import addFieldClass
from z3c.form.widget import FieldWidget
from z3c.form.converter import BaseDataConverter

from plone.app.textfield.interfaces import IRichText, IRichTextValue
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.utils import closest_content

from plone.app.textfield.utils import getAllowedContentTypes
from virtualcollections.interfaces import ILayer

from plone.app.textfield.widget import RichTextWidget


@adapter(IRichText, ILayer)
@implementer(IFieldWidget)
def RichTextFieldWidget(field, request):
    """IFieldWidget factory for RichTextWidget."""
    return FieldWidget(field, RichTextWidget(request))
