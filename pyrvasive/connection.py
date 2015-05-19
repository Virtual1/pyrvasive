#  Pyrvasive
#  -----------
#  Python client for Pervasive SQL databases
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/pyrvasive
#  License: MIT (see LICENSE file)


import pyodbc


class Connection:

    def __init__(self, dsn, debug=False):
        self.dsn = dsn
        self.debug = debug
        if self.debug:
            print "Pyrvasive connect: %s" % (self.dsn)
        self._conn = pyodbc.connect(DSN=self.dsn)
        self._conn.autocommit = False
        self._conn.add_output_converter(pyodbc.SQL_CHAR, lambda s: s.strip())
        self._cursor = self._conn.cursor()
        self.queries = 0

    def __del__(self):
        self._cursor.close()
        self._conn.close()
        if self.debug:
            print "Pyrvasive close: %s" % (self.dsn)

    def execute(self, *args):
        queries = [q for q in args[0].strip().split(";") if q]
        if len(queries) > 1:
            e = "Use executescript() method for multi-statement SQL strings."
            raise Exception(e)
        if self.debug:
            print "Pyrvasive execute:"
            for arg in args:
                print arg
        self.queries += 1
        if args[0].strip().split(" ")[0].upper() == "SELECT":
            return self._cursor.execute(*args)
        return self._cursor.execute(*args).rowcount

    def executescript(self, sql):
        queries = [q for q in sql.strip().split(";") if q]
        rowcount = 0
        for q in queries:
            self.queries += 1
            result = self._cursor.execute(q)
            if result.rowcount:
                rowcount += result.rowcount
        if self.debug:
            print "Pyrvasive executescript:"
            print sql
            print "Pyrvasive executescript: %d rows modified" % (rowcount)
        return rowcount

    def insert(self, table, datadict):
        fields = ", ".join(datadict.keys())
        values = ", ".join('?' for x in range(len(datadict.values())))
        params = datadict.values()
        q = """INSERT INTO "%s" (%s) VALUES (%s);""" % (table, fields, values)
        if self.debug:
            print "Pyrvasive insert: ", q, params
        self.queries += 1
        return self._cursor.execute(q, params).rowcount

    def commit(self):
        if self.debug:
            print "Pyrvasive commit"
        self._conn.commit()

    def rollback(self):
        if self.debug:
            print "Pyrvasive rollback"
        self._conn.rollback()

    @property
    def tables(self):
        tables = self._cursor.tables(tableType='TABLE')
        return tuple([t.table_name for t in tables])

    def columns(self, table):
        q = """
            SELECT TOP 1 *
            FROM "%s"
            """ % table
        cursor = self.execute(q)
        columns = []
        for c in cursor.description:
            columns.append({
                'name': c[0],
                'type': c[1],
                'size': c[3],
                'null': c[6],
            })
        return columns
