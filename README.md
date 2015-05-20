Pyrvasive
=========

Python client for Pervasive SQL databases


Usage
-----

```python
>>> import pyrvasive
```

#### Get a list of all Pervasive Database DSN's configured

```python
>>> pyrvasive.sources()
('DEMODATA', 'MAXDEV', 'MAXDAT')
```

#### Create a database connection object

```python
>>> db = pyrvasive.Connection('DEMODATA')
```

#### List the tables in the database

```python
>>> db.tables
('Billing', 'Class', 'Course', 'Department', 'Enrolls', 'Faculty', 'Person', 'Room', 'Student', 'Tuition')
```

#### Print the column info for the 'Billing' table

```python
>>> for c in db.columns('Billing'):
...     print c['name'], c['type'], c['size'], c['null']
...
Student_ID <class 'decimal.Decimal'> 20 False
Transaction_Number <type 'int'> 5 True
Log <type 'datetime.datetime'> 19 True
Amount_Owed <class 'decimal.Decimal'> 7 True
Amount_Paid <class 'decimal.Decimal'> 7 True
Registrar_ID <class 'decimal.Decimal'> 20 False
Comments <type 'str'> 65500 True
```

#### Basic SELECT

```python
>>> q = """
        SELECT * FROM "Billing"
        WHERE Student_ID = ?;
        """
>>> params = (100062607,)
>>> for row in db.execute(q, params):
...     print row.Amount_Paid, row.Amount_Owed
...
1031.25 2125.00
```

#### Basic DELETE

```python
>>> q = """
        DELETE FROM "Billing"
        WHERE Student_ID = ?;
        """
>>> params = (100062607,)
>>> rows_deleted = db.execute(q, params)
```

#### Basic INSERT

```python
>>> table = 'Enrolls'
>>> data = {
        'Student_ID': 123456,
        'Class_ID':   72,
        'Grade':      91.8,
    }
>>> rows_inserted = db.insert(table, data)
```

#### Execute Multi-Statement SQL String

```python
>>> q = """
        CREATE TABLE "Student Badges" (
            Student_ID CHAR(10) NOT NULL,
            Badge_Num UINT NOT NULL,
            Created TIMESTAMP,
            Log LONGVARCHAR);

        CREATE UNIQUE NOT MODIFIABLE INDEX index1 on "Student Badges"
        (Student_ID ASC);

        CREATE INDEX index2 on "Student Badges"
        (Badge_Num ASC);
        """
>>> db.executescript(q)
```


Testing
-------
The `DEMODATA` database which is installed by default with Pervasive.SQL V8
Server is used to run tests. This database does not have to be located on the
machine running the tests, but an ODBC DSN named `DEMODATA` which is linked to
the database must exist on the machine running the tests.

Execute `python -m unittest discover -v` from the top level pyrvasive directory
to run the tests.

Pyrvasive has currently only been tested with Pervasive.SQL V8 on Windows with
Python 2.7


License
-------
Code is availabe according to the MIT License
(see [LICENSE](https://github.com/ryanss/pyrvasive/raw/master/LICENSE)).
