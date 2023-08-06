import io
import os
import sys

from setuptools import setup, Command, find_packages
from shutil import rmtree


NAME = 'leech_tentacle'
DESCRIPTION = 'the basic modules used to design a new tentacle for the Algernon Leech platform'
URL = 'https://github.com/AlgernonSolutions/leech_tentacle'
EMAIL = 'jcubeta@algernon.solutions'
AUTHOR = 'algernon_solutions/jcubeta'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = '0.0.1'

REQUIRED = [
    'moncrief'
]

EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        # self.status('Building Source and Wheel (universal) distribution…')
        print('Building Source and Wheel (universal) distribution…')
        os.system('python setup.py sdist bdist_wheel --universal')

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        #self.status('Pushing git tags…')
        #os.system('git tag v{0}'.format(about['__version__']))
        #os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    url=URL,
    license='GNU Affero General Public License v3.0',
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    cmdclass={
        'upload': UploadCommand,
    }
)
