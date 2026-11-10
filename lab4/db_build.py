import sqlite3
TOKEN = '5fae7ec0d4cdeb59'
db = sqlite3.connect('lab4.db')
db.executescript('''
DROP VIEW  IF EXISTS employees_public;
DROP TABLE IF EXISTS employees;
CREATE TABLE employees(id INTEGER PRIMARY KEY, name TEXT, dept TEXT,
                       salary INTEGER, home_phone TEXT);
INSERT INTO employees VALUES (1,'Alice','eng',80000,'555-0101'),
                             (2,'Bob',  'eng',60000,'555-0102'),
                             (3,'Carol','hr', 72000,'555-0103');
CREATE VIEW employees_public AS SELECT id, name, dept FROM employees;
''')
db.commit()
print('token:', TOKEN)
print('columns in the table :',
      [d[1] for d in db.execute('PRAGMA table_info(employees)')])
print('columns in the view  :',
      [d[1] for d in db.execute('PRAGMA table_info(employees_public)')])
print('view rows            :',
      db.execute('SELECT * FROM employees_public').fetchall())
print('table rows           :', db.execute('SELECT * FROM employees').fetchall())
print()
print('inference: an aggregate over a group of one is not an aggregate')
for row in db.execute('SELECT dept, COUNT(*), AVG(salary) '
                      'FROM employees GROUP BY dept'):
    print('  dept=%-4s count=%d avg=%.0f' % row)
