from zope.component import adapts
from zope.interface import Interface
from zope.interface.declarations import implementer

from collective.excelexport.exportables.base import BaseExportableFactory
from collective.excelexport.interfaces import IExportable
from plone.dexterity.interfaces import IDexterityFTI


class RBINSDexterityFieldsExportableFactory(BaseExportableFactory):
    """Get fields content schema
    """
    adapts(Interface, Interface, Interface)
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
