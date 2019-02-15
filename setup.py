#! coding: utf-8 

from setuptools import setup


NAME = 'pytropomi'
DESCRIPTION = 'To download TROPOMI Sentinel-5 Product from s5phub'
URL = 'https://github.com/bugsuse/pytropomi'
EMAIL = 'lightning_ly at yahoo dot com'
AUTHOR = 'li yang'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = 0.1

REQUIRED = ['requests', 'tqdm', 'shapely']

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    keywords = ["pthon", "tropomi", "Sentinel-5"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows"
    ],
    platforms = ["any"]
)
