from plone.theme.interfaces import IDefaultPloneLayer

#from virtualcollections import MessageFactory as _

from plone.app.widgets.interfaces import IWidgetsLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3
    browser layer and a plone skin marker.
    """


class ILayer(IWidgetsLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
