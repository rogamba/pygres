#-*- coding: utf-8 -*-
from pygres import Pygres
from datetime import datetime

# SQL Alchemy
config = dict(
    SQL_HOST = '127.0.0.1',
    SQL_DB = 'demo',
    SQL_USER = 'postgres',
    SQL_PASSWORD =  '',
    SQL_PORT="5432",
)

# Testeamos la instancia de pygres
db = Pygres(config)

# Clean DB
db.query(
    """
    DELETE FROM test
    """
)

# Testeamos la asignación de los valores
test = db.model('test','id_test')

# Testeamos savlar un nuevo elemento
print("--------- Saving data...")
test.name = 'Testing row'
test.value = 'Testing value'
test.date = datetime.utcnow()
print(test.values)
test.save()

# Testeamos modificar el elemento
print("--------- Updating data...")
print(test.values)
test.id_test = test.last_id
test.name ='Modified testing name'
test.save()
last_id = test.last_id
print(test.values)

# Test general queries
tests = db.query("SELECT * FROM test").fetch()
print(tests)

# Test specific queries
print("---------- Getting values...")
last_id = test.last_id
test2 = db.model('test','id_test')
test2.get(last_id)
print(test2.values)

# Test not commit
print("----------- Insert 3, do not commit")
for i in range(0,2):
    test3 = db.model('test','id_test')
    test3.name = 'Testing uncommited row %s ' % (i,)
    test3.value = 'Uncommited row %s ' % (i,)
    test3.date = datetime.utcnow()
    test3.save(commit=False)
test3.rollback()

print("----------- Insert 3, commit!")
for i in range(0,5):
    test3 = db.model('test','id_test')
    test3.name = 'Testing commited row %s ' % (i,)
    test3.value = 'Commited row %s ' % (i,)
    test3.date = datetime.utcnow()
    test3.save()
test3.commit()

print("----------- Delete last record: %s " % test3.last_id)
test4 = db.model('test','id_test')
test4.id_test = test3.last_id
test4.delete()


db.close()
