import os
from distutils.core import setup

from djmx import __version__


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(name='django-mx-datetime',
      version=__version__,
      description='Provides date/time/datetime related fields using mx.DateTime for Django databases',
      long_description=read_file('README.md'),
      author='Justin Quick',
      author_email='justquick@gmail.com',
      url='http://github.com/justquick/django-mx-datetime',
      packages=['djmx', 'djmx.runtests'],
      install_requires=read_file('requirements.txt'),
      zip_safe=False,
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Database'],
      )
