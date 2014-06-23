from setuptools import (
    find_packages,
    setup,
)
from curator import __version__

setup(
    name='curator',
    version=__version__,
    description='Helper for working with lua scripts.',
    packages=find_packages(),
    setup_requires=[
        'nose>=1.0',
        'coverage>=1.0',
        'ipython==0.13.2',
        'ipdb==0.8',
    ],
    install_requires=[
        'redis==2.10.1',
        'jinja2==2.7.2',
    ],
)
