import os

from setuptools import setup, find_packages

version = "1.0dev"


def read(*rnames):
    return open(
        os.path.join(".", *rnames)
    ).read()


long_description = "\n\n".join(
    [read("README.rst"),
     read("docs", "INSTALL.rst"),
     read("docs", "CHANGES.rst")]
)

classifiers = [
    "Framework :: Plone",
    "Framework :: Plone :: 4.0",
    "Framework :: Plone :: 4.1",
    "Framework :: Plone :: 4.2",
    "Framework :: Plone :: 4.3",
    "Programming Language :: Python",
    "Topic :: Software Development"]

name = "virtualcollections"
setup(
    name=name,
    namespace_packages=[
    ],
    version=version,
    description="virtualcollections",
    long_description=long_description,
    classifiers=classifiers,
    keywords="",
    author="kiorky <kiorky@cryptelium.net>",
    author_email="kiorky@cryptelium.net",
    url="http://www.generic.com",
    license="GPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "setuptools",
        "z3c.autoinclude",
        "Plone",
        "chardet",
        "plone.app.upgrade",
        "plone.app.themingplugins",
        "collective.dexteritytextindexer",
        "plone.app.dexterity [relations]",
        "plone.app.referenceablebehavior",
        "plone.directives.dexterity",
        "plone.directives.form",
        "plone.app.theming",
        "plone.app.themingplugins",
        # with_ploneproduct_cjqui
        "collective.js.jqueryui",
        # with_ploneproduct_ckeditor
        "collective.ckeditor",
        # with_ploneproduct_eeafn
        "python-dateutil",
        "collective.bibliocustomviews",
        "collective.googleanalytics",
        "collective.dexteritytextindexer",
        "eea.facetednavigation",
        # with_binding_pil
        "Pillow",
        # with_ploneproduct_datatables
        "collective.js.datatables",
        # with_ploneproduct_pacaching
        "plone.app.caching",
        # with_ploneproduct_plomino
        'plone.app.widgets[archetypes,dexterity]',
        "collective.zipfiletransport",
        "plone.app.contenttypes",
        'Products.ImageEditor',
        'Products.PloneKeywordManager',
        "plone.app.ldap",
        'rbins_masschange',
        # -*- Extra requirements: -*-
        "plomino.tinymce",
        "Products.CMFPlomino",
    ],
    extras_require={
        "test": ["plone.app.testing", "ipython"]
    },
    entry_points={
        "z3c.autoinclude.plugin": ["target = plone"],
    },
)
# vim:set ft=python:
