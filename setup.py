import os, sys
from setuptools import setup, find_packages

VERSION = '0.2dev'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


setup(name='ploudenv.themegallery',
      version='0.2.0',
      description='Ploud theme gallery',
      long_description=README + '\n\n' +  CHANGES,
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
        'plone.app.registry',
      ],
      entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
      """,
      )
