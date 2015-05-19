#  Pyrvasive
#  -----------
#  Python client for Pervasive SQL databases
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/pyrvasive
#  License: MIT (see LICENSE file)


__version__ = '0.1-dev'


import pyodbc

from connection import Connection


def sources():
    databases = pyodbc.dataSources().items()
    return tuple([dsn for dsn, desc in databases if 'Pervasive' in desc])
