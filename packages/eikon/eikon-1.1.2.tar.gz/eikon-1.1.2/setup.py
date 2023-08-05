# coding: utf-8

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import re


# NoseTestCommand allow to launch nosetest with the command 'python setup.py test'
class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])

try:
    from pypandoc import convert_file
    read_md = lambda f: convert_file(f, 'rst')
    description_content_type = None
except ImportError:
    print('##########################################################################')
    print("## warning: pypandoc module not found, could not convert Markdown to RST #")
    print('##########################################################################')
    print("")
    read_md = lambda f: open(f, 'r').read()
    description_content_type="text/markdown"


module_file = open("eikon/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", module_file))

setup(name='eikon',
      version=metadata['version'],
      description='Python package for retrieving Eikon data.',
      long_description=read_md('README.md'),
      long_description_content_type=description_content_type,
      url='https://developers.refinitiv.com/eikon-apis/eikon-data-api',
      author='REFINITIV',
      author_email='',
      license='Apache 2.0',
      data_files=[("", ["LICENSE.md"])],
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      use_2to3=True,
      zip_safe=False,
      install_requires=['requests==2.22.0',
                        'requests-async==0.6.2',
                        'nest_asyncio==1.0.0',
                        'datetime',
                        'pandas>=0.17.0',
                        'numpy>=1.11.0',
                        'appdirs==1.4.3',
                        'python-dateutil',
                        'websocket-client',
                        'deprecation'],
      test_suite='nose.collector',
      tests_require=['nose', 'mock', 'lettuce'],
      cmdclass={'test': NoseTestCommand}
)