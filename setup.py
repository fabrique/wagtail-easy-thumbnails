import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Dynamically calculate the version based on django.VERSION.
version = __import__('wagtail_easy_thumbnails').get_version()

setup(
    name='wagtail-easy-thumbnails',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Use easy_thumbnails with Django Wagtail images',
    long_description=README,
    author='Robin van der Rijst - Fabrique',
    author_email='robinr@fabrique.nl',
    url='https://github.org/fabrique/wagtail-easy-thumbnails',
    install_requires=[
            'wagtail>=1.5',
            'easy_thumbnails>=2.3',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
