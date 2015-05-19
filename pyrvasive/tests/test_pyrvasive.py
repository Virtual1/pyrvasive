#  Pyrvasive
#  -----------
#  Python client for Pervasive SQL databases
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/pyrvasive
#  License: MIT (see LICENSE file)


import threading
import unittest

import pyrvasive


class TestPyrvasive(unittest.TestCase):

    def setUp(self):
        # Uses default DEMODATA dababase installed with Pervasive server
        self.db = pyrvasive.Connection('DEMODATA')


    def test_demodata(self):
        self.assertIn('DEMODATA', pyrvasive.sources())
        self.assertIsNotNone(self.db)


    def test_select(self):
        q = """
            SELECT *
            FROM "Billing"
            """
        rows = self.db.execute(q).fetchall()

        # Test that 1315 rows were returned
        self.assertEqual(len(rows), 1315)

        # Test that each row has 7 columns
        self.assertEqual(len(rows[0]), 7)

        q = """
            SELECT Student_ID, Log, Amount_Owed, Comments
            FROM "Billing"
            WHERE Amount_Owed >= 5000
            """
        rows = self.db.execute(q).fetchall()

        # Test that only 52 rows were returned
        self.assertEqual(len(rows), 52)

        # Test that only 4 columns were returned
        self.assertEqual(len(rows[0]), 4)


    def test_insert(self):
        table = 'Enrolls'
        data = {
            'Student_ID': 123,
            'Class_ID':   456,
            'Grade':      95.3,
        }

        # Test that 1 row of data was inserted
        self.assertEqual(self.db.insert(table, data), 1)

        # Test that we can select this new (uncommitted) inserted row
        # and that the data inserted is correct
        q = """
            SELECT *
            FROM "Enrolls"
            WHERE Student_ID = 123
            """
        row = self.db.execute(q).fetchone()
        self.assertEqual(row.Student_ID, data['Student_ID'])
        self.assertEqual(row.Class_ID, data['Class_ID'])
        self.assertEqual(round(row.Grade, 1), data['Grade'])
        self.db.rollback()


    def test_tables(self):
        tables = ('Billing', 'Class', 'Course', 'Department', 'Enrolls',
                  'Faculty', 'Person', 'Room', 'Student', 'Tuition')
        self.assertEqual(self.db.tables, tables)


    def test_columns(self):
        columns = ('Student_ID', 'Transaction_Number', 'Log', 'Amount_Owed',
                   'Amount_Paid', 'Registrar_ID', 'Comments')
        db_columns = tuple([c['name'] for c in self.db.columns('Billing')])
        self.assertEqual(db_columns, columns)

        sizes = (20, 5, 19, 7, 7, 20, 65500)
        db_sizes = tuple([c['size'] for c in self.db.columns('Billing')])
        self.assertEqual(db_sizes, sizes)

        nulls = (False, True, True, True, True, False, True)
        db_nulls = tuple([c['null'] for c in self.db.columns('Billing')])
        self.assertEqual(db_nulls, nulls)


    def test_concurrency(self):

        def inserter(student_id):
            idb = pyrvasive.Connection(self.db.dsn)
            # Insert 500 rows
            for i in range(500):
                table = 'Enrolls'
                data = {
                    'Student_ID': student_id,
                    'Class_ID':   i,
                    'Grade':      99.9,
                }
                self.assertEqual(idb.insert(table, data), 1)
                idb.commit()
            q = """
                DELETE FROM "Enrolls"
                WHERE Student_ID = ?
                """
            params = (student_id,)
            # Test that 500 rows are deleted
            self.assertEqual(idb.execute(q, params), 500)
            idb.commit()

        def selecter(student_id):
            sdb = pyrvasive.Connection(self.db.dsn)
            found_id = False
            found_999 = False
            for i in range(1000):
                q = """
                    SELECT * FROM "Enrolls"
                    WHERE Student_ID = ?
                    """
                params = (student_id,)
                if sdb.execute(q, params).fetchone():
                    found_id = True
                params = (999,)
                if sdb.execute(q, params).fetchone():
                    found_999 = True
            # Test that Student_ID from inserter() was found
            self.assertTrue(found_id)
            self.assertFalse(found_999)

        threads = [
            threading.Thread(target=inserter, args=(123,)),
            threading.Thread(target=inserter, args=(456,)),
            threading.Thread(target=selecter, args=(123,)),
            threading.Thread(target=selecter, args=(456,)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


    def test_executescript(self):
        table = 'Enrolls'
        data = {'Student_ID': 123, 'Class_ID': 5, 'Grade': 99.9}
        self.db.insert(table, data)
        data = {'Student_ID': 456, 'Class_ID': 5, 'Grade': 99.9}
        self.db.insert(table, data)
        data = {'Student_ID': 789, 'Class_ID': 5, 'Grade': 99.9}
        self.db.insert(table, data)
        q = """
            DELETE FROM "Enrolls" WHERE Student_ID = 123;
            DELETE FROM "Enrolls" WHERE Student_ID = 456;
            DELETE FROM "Enrolls" WHERE Student_ID = 789;
            DELETE FROM "Enrolls" WHERE Student_ID = 999;
            """
        # Check that error is raised when using execute() method
        self.assertRaises(Exception, self.db.execute, q)
        # Check that 3 rows are modified (deleted)
        self.assertEqual(self.db.executescript(q), 3)
        self.db.rollback()
