# encoding: utf-8

import os
from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from distutils.core import Command
from distutils.sysconfig import get_python_lib
from pkg_resources import resource_filename


class InstallRise(install):
    def run(self):
        install.run(self)

    sub_commands = install.sub_commands + [('install_extension', lambda self: True)]


class DevelopRise(develop):
    def run(self):
        develop.run(self)
        source = os.path.join(self.egg_path, 'livereveal')
        InstallExtension(self.distribution, source=source).run()


class InstallExtension(Command):
    user_options = [
        # Select installation scheme and set base director(y|ies)
        ('develop', None,
         "Install livereal as a symlink to the source."),
        ('no-enable', None,
         "(Unix only) prefix for platform-specific files")]

    boolean_options = ['develop', 'no-enable']

    def __init__(self, distribution, source=None):
        Command.__init__(self, distribution)
        self.source = source

    def initialize_options(self):
        self.develop = None
        self.no_enable = None

    def finalize_options(self):
        pass

    def get_outputs(self):
        return []

    def run(self):
        from notebook.nbextensions import install_nbextension
        if self.source:
            livereveal_dir = self.source
        else:
            lib_dir = os.path.join(get_python_lib(), 'livereveal')
            if os.path.exists(lib_dir):
                livereveal_dir = lib_dir
            else:
                livereveal_dir = os.path.join(os.path.dirname(__file__), 'livereveal')
        install_nbextension(livereveal_dir, symlink=self.develop,
                            overwrite=self.develop, user=True)

        if not self.no_enable:
            from notebook.services.config import ConfigManager
            cm = ConfigManager()
            cm.update('notebook', {"load_extensions": {"livereveal/main": True}})


setup(name='livereveal',
      version='0.0.1',
      description='"Live" Reveal.js Jupyter/IPython Slideshow Extension',
      author=u'Damián Avila',
      url='https://github.com/damianavila/RISE',
      long_description=open('README.md').read(),
      cmdclass={'install': InstallRise,
                'develop': DevelopRise,
                'install_extension': InstallExtension},
      setup_requires=['notebook'],
      packages=['livereveal'],
      package_data={'livereveal': ['main.js',
                                   '*.css',
                                   'reveal.js/css/*.css',
                                   'reveal.js/css/print/*.css',
                                   'reveal.js/css/theme/*.css',
                                   'reveal.js/js/*.js',
                                   'reveal.js/lib/*/*',
                                   'reveal.js/plugin/*/*']},
      zip_safe=False,
      keywords='python jupyter ipython javascript nbextension extension',
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'License :: OSI Approved'],
)
