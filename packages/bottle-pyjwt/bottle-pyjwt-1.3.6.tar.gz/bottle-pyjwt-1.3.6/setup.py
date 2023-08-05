# coding: utf-8
import re
from os import path as op
from setuptools import setup, find_packages


class File:
    __cache__ = None
    def __init__(self, file):
        self.file = file

    @property
    def text(self):
        if self.__cache__ is None:
            try:
                self.__cache__ = open(op.join(op.dirname(__file__), self.file)).read()
            except IOError:
                self.__cache__ = ""
        return self.__cache__

    def __getattribute__(self, attr):
        for attr in (attr, attr.upper(), "__{}__".format(attr), "__{}__".format(attr.upper())):
            try:
                return super(File, self).__getattribute__(attr)
            except AttributeError:
                search = re.search('^{}\s*=\s*(.*)'.format(attr), self.text, re.M)
                if search is not None:
                    return search.group(1).replace('"', '').replace("'", '')
        return ""

    def __str__(self):
        return self.text


MODULE = File('bottle_jwt.py')
README_RST = File('README.rst')
README_MD = File('README.md')
README_TXT = File('README.txt')
REQUIREMENTS = File('requirements.txt')
REQUIREMENTS_EGG = File('{}.egg-info/requires.txt'.format(MODULE.name.replace('-', '_') or MODULE.project.replace('-', '_')))


setup(
    # Project Metadata
    name = MODULE.name or MODULE.project,
    version = MODULE.version,
    url = MODULE.url,
    download_url = MODULE.download,

    # Autor Metadata
    author = MODULE.author,
    author_email = MODULE.author_email,
    maintainer = MODULE.maintainer,
    maintainer_email = MODULE.maintainer_email,
    license = "MIT",
    license_file = "LICENSE",

    # Description Metadata
    description = MODULE.description,
    long_description = str(README_RST) or str(README_MD) or str(README_TXT),
    long_description_content_type = "text/x-rst" if str(README_RST) else "text/markdown" if str(README_MD) else "text/plain",

    # Package Metadata
    packages = find_packages(), # exclude = ['*'], include = ['*']
    py_modules = ['bottle_jwt', 'bottle_jwt_version'],
    package_data = {},
    include_package_data = False,
    exclude_package_data = {},
    install_requires = [l for l in str(REQUIREMENTS).splitlines() if l and not l.startswith('#')] or
                       [l for l in str(REQUIREMENTS_EGG).splitlines() if l and not l.startswith('#')],
    extras_require = {},
    # python_requires = "",
    setup_requires = ['scmver'],
    scmver={"local": "{local:%Y.%m.%d}",
            "write_to": "bottle_jwt_version.py",
            "fallback": "bottle_jwt_version:version"
            },

    # Keywords Metadata
    platforms = [],
    keywords = [],
    classifiers = []
)
