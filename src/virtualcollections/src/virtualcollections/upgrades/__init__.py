# -*- coding: utf-8 -*-

import datetime
import re
import logging
from ecreall.helpers.upgrade.interfaces import IUpgradeTool

#try:
#    from Products.CMFPlone.migrations import migration_util
#except:
#    #plone4
#    from plone.app.upgrade import utils as migration_util

from Products.CMFCore.utils import getToolByName
import transaction


from Products.Archetypes.interfaces.field import ITextField
from Products.GenericSetup.utils import _resolveDottedName
from Testing.makerequest import makerequest
from StringIO import StringIO

from plone.app.textfield import IRichText, RichTextValue
from plone.dexterity.utils import iterSchemata
from plone.portlet.static.static import IStaticPortlet
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from zope.component import getUtility, getMultiAdapter
from zope.schema import getFieldsInOrder
from zope.schema.interfaces import IText

re_flags = re.U | re.M | re.S | re.X
PRODUCT = 'virtualcollections'
PROFILE = '%s:default' % PRODUCT
PROFILEID = 'profile-%s' % PROFILE


def log(message, level='info'):
    logger = logging.getLogger('%s.upgrades' % PRODUCT)
    getattr(logger, level)(message)


def commit(context):
    transaction.commit()
    context._p_jar.sync()


def move(context, oldid, newid):
    purl = getToolByName(context, 'portal_url')
    pobj = purl.getPortalObject()
    log(
        'Renaming %s to %s in %s (%s)' % (
            oldid, newid,
            '/'.join(context.getPhysicalPath()), pobj.getId())
    )
    context.manage_renameObject(oldid, newid)


def move_custom(context, ignores=None):
    log('Moving away custom content in portalskin')
    if not ignores:
        ignores = [
            '\.(jpeg|jpg|JPG|JPEG|png|PNG|GIF|gif|old)$'
        ]
    dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    plone = getToolByName(context, 'portal_url').getPortalObject()
    custom = plone['portal_skins']['custom']
    ids = custom.objectIds()
    MARKER = '%s-RENAMED' % PRODUCT.replace('.', '')
    marker = MARKER.lower()
    ignores.extend([MARKER, marker])
    for id in ids:
        moved = True
        for i in ignores:
            if (
                re.search(i, id, re_flags)
                or re.search(i, id.lower(), re_flags)
            ):
                moved = False
        if moved:
            move(custom, id,
                 '%s_%s.%s.disabled' % (MARKER, dt, id,))


def remove_persistent_utilities(ctx,
                                searchs=None):
    context = getToolByName(ctx, 'portal_url').getPortalObject()
    if not searchs:
        searchs = []
    sm = context.getSiteManager()
    changed = False
    adapters = sm.utilities._adapters
    subscribers = sm.utilities._subscribers
    provided = sm.utilities._provided
    for k in searchs:
        for x in adapters[0].keys():
            if k.search(x.__module__):
                changed = True
                log("Deleting %s" % x)
                del adapters[0][x]
        for x in subscribers[0].keys():
            if k.search(x.__module__):
                changed = True
                log("Deleting %s" % x)
                del subscribers[0][x]
        for x in provided.keys():
            if k.search(x.__module__):
                changed = True
                log("Deleting %s" % x)
                del provided[x]
    if changed:
        sm.utilities._adapters = adapters
        sm.utilities._subscribers = subscribers
        sm.utilities._provided = provided
    commit(context)


def cleanup_portal_setup_registries(context,
                                    do_import_steps=True,
                                    do_export_steps=True,
                                    do_toolset=True):
    toremove = ['plonepas']
    p = portal_setup = getToolByName(context, 'portal_setup')
    p.applyContextById(p.getBaselineContextID())
    import_steps = dict(
        [(a, portal_setup.getImportStepMetadata(a))
         for a in portal_setup.getSortedImportSteps()])
    export_steps = dict(
        [(a, portal_setup.getExportStepMetadata(a))
         for a in portal_setup.listExportSteps()])
    for (test, registry, pregistry) in [
        [do_import_steps, import_steps, p._import_registry],
        [do_export_steps, export_steps, p._export_registry],
    ]:
        if test:
            invalids = registry.copy()
            for a in invalids.keys():
                try:
                    if (
                        not invalids[a].get("invalid", False)
                        and not a in toremove
                    ):
                        del invalids[a]
                except:
                    if invalids[a] is not None:
                        raise
            for item in invalids:
                log('Removing %s from %s' % (
                    item, pregistry.__class__.__name__))
                remove = item in pregistry._registered
                if remove:
                    pregistry.unregisterStep(item)
    if do_toolset:
        toolset = p._toolset_registry
        for l in ['_required', '_forbidden']:
            invalids = {}
            reg = getattr(toolset, l)
            for item in reg:
                data = reg[item]
                if _resolveDottedName(data['class']) is None:
                    invalids[item] = data
            for item in invalids:
                log(
                    'Removing from toolset.%s: %s (%s %s)' % (
                        l,
                        item,
                        invalids[item]['id'],
                        invalids[item]['class'],
                    )
                )
                del reg[item]
                setattr(toolset, l, reg)
    commit(context)


def quickinstall_addons(context,
                        install=None,
                        uninstall=None,
                        upgrades=None):
    qi = getToolByName(context, 'portal_quickinstaller')

    if install is not None:
        for addon in install:
            if qi.isProductInstallable(addon):
                qi.installProduct(addon)
                log('Installed %s' % addon)
            else:
                log('%s can t be installed' % addon, 'error')

    if uninstall is not None:
        for p in uninstall:
            if qi.isProductInstalled(p):
                qi.uninstallProducts([p])
                log('Uninstalled %s' % p)

    if upgrades is not None:
        if upgrades in ("all", True):
            # find which addons should be upgrades
            installedProducts = qi.listInstalledProducts(showHidden=True)
            upgrades = [p['id'] for p in installedProducts]
        for upgrade in upgrades:
            # do not try to upgrade myself -> recursion
            if upgrade == PRODUCT:
                continue
            try:
                qi.upgradeProduct(upgrade)
                log('Upgraded %s' % upgrade)
            except KeyError:
                log('can t upgrade %s' % upgrade, 'error')


def recook_resources(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    jsregistry = getToolByName(site, 'portal_javascripts')
    cssregistry = getToolByName(site, 'portal_css')
    jsregistry.cookResources()
    cssregistry.cookResources()
    log('Recooked css/js')


def import_js(context):
    """
    """
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(
        PROFILEID, 'jsregistry', run_dependencies=False)
    log('Imported js')


def import_css(context):
    """
    """
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(
        PROFILEID, 'cssregistry', run_dependencies=False)
    log('Imported css')


def upgrade_profile(context, profile_id, steps=None):
    """
    """
    portal_setup = getToolByName(context.aq_parent, 'portal_setup')
    gsteps = portal_setup.listUpgrades(profile_id)

    class fakeresponse(object):
        def redirect(self, *a, **kw):
            pass

    class fakerequest(object):
        RESPONSE = fakeresponse()

        def __init__(self):
            self.form = {}
            self.get = self.form.get
    fr = fakerequest()
    if steps is None:
        steps = []
        for col in gsteps:
            if not isinstance(col, list):
                col = [col]
            for ustep in col:
                steps.append(ustep['id'])
        fr.form.update({
            'profile_id': profile_id,
            'upgrades': steps,
        })
    portal_setup.manage_doUpgrades(fr)


def upgrade_plone(portal_setup):
    """
    """
    out = StringIO()
    portal = makerequest(
        getToolByName(
            portal_setup, 'portal_url'
        ).getPortalObject(),
        stdout=out,
        environ={'REQUEST_METHOD': 'POST'})
    # pm = getToolByName(portal, 'portal_migration')
    # use direct acquisition for REQUEST to be always there
    pm = portal.portal_migration
    report = pm.upgrade(dry_run=False)
    return report


def upgrade_1001(context):
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_setup = site.portal_setup

    portal_setup.runAllImportStepsFromProfile(
        'profile-collective.js.jqueryui:default')
    portal_setup.runAllImportStepsFromProfile(
        'profile-collective.js.datatables:default')
    portal_setup.runAllImportStepsFromProfile(
        'profile-collective.bibliocustomviews:default')
    import_css(context)
    import_js(context)
    recook_resources(context)


def upgrade_1002(context):
    tool = IUpgradeTool(context)
    tool.runImportStep('virtualcollections', 'viewlets')


def upgrade_1003(context):
    tool = IUpgradeTool(context)
    tool.runImportStep('virtualcollections', 'viewlets')
    tool.runImportStep('virtualcollections', 'propertiestool')
    tool.runImportStep('virtualcollections', 'actions')
    recook_resources(context)


# From https://github.com/collective/collective.searchandreplace/blob/master/collective/searchandreplace/searchreplaceutility.py
def _replaceText(matcher, text, rtext):
    """ Replace instances """
    newtext = ""
    mindex = 0
    repl_count = 0
    mobj = matcher.finditer(text)
    for x in mobj:
        start, end = x.span()
        newtext += text[mindex:start]
        newtext += rtext
        mindex = end
    newtext += text[mindex:]
    return newtext


def upgrade_1004(context):
    """ Replace http:// and https:// to // in bodies """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_catalog = getToolByName(context, 'portal_catalog')
    matcher = re.compile('https?://', re.IGNORECASE)

    # Replace in Page
    brains = portal_catalog.unrestrictedSearchResults(portal_type='Document')
    for brain in brains:
        obj = brain.getObject()
        for schemata in iterSchemata(obj):
            fields = getFieldsInOrder(schemata)
            for name, field in fields:
                if IRichText.providedBy(field) or IText.providedBy(field):
                    baseunit = getattr(field.interface(obj), field.__name__)
                    text = getattr(baseunit, "raw", baseunit)

                    new_text = _replaceText(matcher, text, '//')

                    if IRichText.providedBy(field):
                        old = field.get(obj)
                        if old is None:
                            new_text = RichTextValue(new_text)
                        else:
                            new_text = RichTextValue(new_text, old.mimeType, old.outputMimeType)
                    setattr(field.interface(obj), field.__name__, new_text)

    # Replace in portlets
    def replace_portlet_text(context):
        for manager_name in [
            "plone.leftcolumn",
            "plone.rightcolumn",
            "ContentWellPortlets.InHeaderPortletManager1",
            "ContentWellPortlets.InHeaderPortletManager2",
            "ContentWellPortlets.InHeaderPortletManager3",
            "ContentWellPortlets.InHeaderPortletManager4",
            "ContentWellPortlets.InHeaderPortletManager5",
            "ContentWellPortlets.InHeaderPortletManager6",
            "ContentWellPortlets.AbovePortletManager1",
            "ContentWellPortlets.AbovePortletManager2",
            "ContentWellPortlets.AbovePortletManager3",
            "ContentWellPortlets.AbovePortletManager4",
            "ContentWellPortlets.AbovePortletManager5",
            "ContentWellPortlets.AbovePortletManager6",
            "ContentWellPortlets.BelowPortletManager1",
            "ContentWellPortlets.BelowPortletManager2",
            "ContentWellPortlets.BelowPortletManager3",
            "ContentWellPortlets.BelowPortletManager4",
            "ContentWellPortlets.BelowPortletManager5",
            "ContentWellPortlets.BelowPortletManager6",
            "ContentWellPortlets.FooterPortletManager1",
            "ContentWellPortlets.FooterPortletManager2",
            "ContentWellPortlets.FooterPortletManager3",
            "ContentWellPortlets.FooterPortletManager4",
            "ContentWellPortlets.FooterPortletManager5",
            "ContentWellPortlets.FooterPortletManager6",
        ]:
            manager = getUtility(IPortletManager, name=manager_name, context=context)
            mapping = getMultiAdapter((context, manager), IPortletAssignmentMapping)

            for id, assignment in mapping.items():
                if IStaticPortlet.providedBy(assignment):
                    text = assignment.text
                    new_text = _replaceText(matcher, text, '//')
                    assignment.text = new_text

    replace_portlet_text(site)
    brains = portal_catalog.unrestrictedSearchResults(portal_type=['Folder', 'Document'])
    for brain in brains:
        obj = brain.getObject()
        replace_portlet_text(obj)
