from zope.component import adapts
from zope.interface import Interface
from zope.interface.declarations import implementer
from zope.schema.interfaces import ICollection, IText

from collective.excelexport.exportables.base import BaseExportableFactory
from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer
from collective.excelexport.interfaces import IExportable
from plone import api
from plone.app.textfield.interfaces import IRichText
from plone.dexterity.interfaces import IDexterityFTI
from z3c.form.interfaces import NO_VALUE
from Products.CMFPlone.utils import safe_unicode

from .interfaces import ILayer


class RBINSDexterityFieldsExportableFactory(BaseExportableFactory):
    """Get fields content schema
    """
    adapts(Interface, Interface, ILayer)
    weight = 1

    def get_exportables(self):
        return [PathRenderer()]


@implementer(IExportable)
class PathRenderer(object):
    def render_header(self):
        """Gets the value to render on the first row of excel sheet for this field
        """
        return "Path"

    def render_value(self, obj):
        """Gets the value to render in excel file from content
        """
        return '/' + '/'.join(obj.getPhysicalPath()[2:])

    def render_style(self, obj, base_style):
        """Gets the style rendering of the
        base_style is the default style of a cell for content
        """
        return base_style


class SubjectsRenderer(BaseFieldRenderer):
    adapts(ICollection, Interface, ILayer)

    def render_value(self, obj):
        return u'\n'.join(obj.subject)


class TextFieldRenderer(BaseFieldRenderer):
    adapts(IText, Interface, ILayer)

    def _get_text(self, value):
        return value

    def render_value(self, obj):
        """Gets the value to render in excel file from content value
        """
        value = self.get_value(obj)
        if not value or value == NO_VALUE:
            return ""

        return safe_unicode(self._get_text(value))


class RichTextFieldRenderer(TextFieldRenderer):
    adapts(IRichText, Interface, ILayer)

    def _get_text(self, value):
        return value.raw
        # ptransforms = api.portal.get_tool('portal_transforms')
        # return ptransforms.convert('html_to_text', value.output).getData().strip()
