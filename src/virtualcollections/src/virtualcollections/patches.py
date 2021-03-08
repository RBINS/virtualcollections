

try:
    import Products.PDBDebugMode.pdblogging
    import re

    Products.PDBDebugMode.pdblogging._mars_old_matchers = Products.PDBDebugMode.pdblogging.ignore_matchers
    Products.PDBDebugMode.pdblogging.ignore_matchers = Products.PDBDebugMode.pdblogging._mars_old_matchers + (
    re.compile(r"Couldn't load state for").search, re.compile("No blob file").search)
except ImportError:
    print("Products.PDBDebugMode.pdblogging not available")
    pass


import plone.app.widgets.dx

plone.app.widgets.dx.AjaxSelectWidget.separator = ';;;'
