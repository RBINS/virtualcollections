from zope import interface
#from zope import schema
from plone.theme.interfaces import IDefaultPloneLayer

#from virtualcollections import MessageFactory as _
from z3c.form.interfaces import IFormLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3
    browser layer and a plone skin marker.
    """


class ILayer(IFormLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
