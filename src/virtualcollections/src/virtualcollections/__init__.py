import logging
from zope.i18nmessageid import MessageFactory

MessageFactory = virtualcollectionsMessageFactory = MessageFactory('virtualcollections')
logger = logging.getLogger('virtualcollections')
EXTENSION_PROFILES = ('virtualcollections:default',)
SKIN = 'skin'
PRODUCT_DEPENDENCIES = (
)

import patches

def initialize(context):
    """Initializer called when used as a Zope 2 product."""


GLOBALS = globals()
