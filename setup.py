#  Pyrvasive
#  -----------
#  Python client for Pervasive SQL databases
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/pyrvasive
#  License: MIT (see LICENSE file)


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name = 'Pyrvasive',
    version = '0.1-dev',
    url = 'https://github.com/ryanss/pyrvasive',
    author = 'ryanss',
    author_email = 'ryanssdev@icloud.com',
    description = 'Python client for Pervasive SQL databases',
    long_description = 'Python client for Pervasive SQL databases',
    license = 'MIT',
    packages = ['pyrvasive'],
    install_requires = ['pyodbc'],
    platforms = 'Win32',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
