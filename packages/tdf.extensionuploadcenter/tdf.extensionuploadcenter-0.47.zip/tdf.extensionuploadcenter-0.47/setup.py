# -*- coding: utf-8 -*-
"""Installer for the tdf.extensionuploadcenter package."""

from setuptools import setup, find_packages


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])


setup(name='tdf.extensionuploadcenter',
      version='0.47',
      description="TDF Extension Upload Center",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone Add-On LibreOffice extension extensionuploadcenter',
      author='Andreas Mantke',
      author_email='maand@gmx.de',
      url='http://github.com/tdf/tdf.extensionuploadcenter',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tdf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.namedfile [blobs]',
          # -*- Extra requirements: -*-
          'collective.dexteritytextindexer',
          'cioppino.twothumbs',
          'plone.formwidget.recaptcha',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
