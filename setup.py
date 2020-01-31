from setuptools import setup, find_packages
import os
import re

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, "swagccg", "src", "__init__.py")) as f:
    VERSION = re.search(r"__version__ = '(.+?)'", f.read()).group(1)

name = 'swagccg'
setup(
    name=name,  # Required
    version=VERSION,
    description='Swagger Client Code Generator. Using Python. For Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/erkandem/swagccg-py2py',
    author='Erkan Demiralay',
    author_email='erkan.dem@pm.me',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='REST api-client client-code code-generator swagger openapi',
    packages=find_packages(exclude=['swagccg.docs', 'swagccg.tests']),
    # install_requires=['peppercorn'],
    # extras_require={  # Optional
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },
    # package_data={  # Optional
    #    'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # Optional
    # entry_points={  # Optional
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    # },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/erkandem/swagccg-py2py/issues',
        'Source': 'https://github.com/erkandem/swagccg-py2py/',
        'Documentation': 'https://erkandem.github.io/swagccg-py2py/',
    },
)
