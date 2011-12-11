import os, sys
from setuptools import setup, find_packages

VERSION = '0.2dev'

here = os.path.abspath(os.path.dirname(__file__))
long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')


setup(name='ploudenv.themegallery',
      version='0.1.0',
      description='Ploud theme gallery',
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        ],
      author='Nikolay Kim',
      author_email='Nikolay Kim <nikolay@enfoldsystems.com>',
      url='http://www.enfoldsystems.com',
      packages=find_packages(),
      namespace_packages=['ploudenv'],
      zip_safe=False,
      include_package_data=True,
      install_requires = [
        'setuptools',
        'simplejson',
        'Products.CMFPlone',
        'plone.app.theming',
      ],
      entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
      """,
      )
