#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout import viewlets
from plone.app.layout.viewlets import content


class ViewletBaseMixin:
    """."""


class ViewletBase(viewlets.ViewletBase, ViewletBaseMixin):
    """."""


LOGO_ID = 'marslogo.png'
class LogoViewlet(ViewletBase):
    index = ViewPageTemplateFile('logo.pt')
    def update(self):
        super(LogoViewlet, self).update()
        portal = self.portal_state.portal()
        logoTitle = self.portal_state.portal_title()
        self.src = LOGO_ID
        self.navigation_root_title = self.portal_state.navigation_root_title()


class DocumentBylineViewlet(ViewletBase, content.DocumentBylineViewlet):
    '''.'''
    index = ViewPageTemplateFile('document_byline.pt')

#from plone.app.layout.viewlets.common import ViewletBase
