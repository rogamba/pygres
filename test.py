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
# you can send the parameter clear=False if you want the object to keep populates
test.save()

# Testeamos savlar un nuevo elemento
#print("--------- Saving data defining primary_key...")
#test.id_test = 100
#test.name = 'Testing row defininf pk'
#test.value = 'Testing value defining pk'
#test.date = datetime.utcnow()
#print(test.values)
# you can send the parameter clear=False if you want the object to keep populates
#test.save()

# Testeamos modificar el elemento
print("\n--------- Updating data...")
print(test.values)
test.id_test = test.last_id
test.name ='Modified testing name'
test.save(clear=False)
last_id = test.last_id
print(test.values)

# Test general queries
tests = db.query("SELECT * FROM test").fetch()
print(tests)

# Test specific queries
print("\n---------- Getting values...")
last_id = test.last_id
test2 = db.model('test','id_test')
test2.get(last_id)
print(test2.values)

# Test not commit
print("\n----------- Insert 3, do not commit")
test3 = db.model('test','id_test')
for i in range(0,2):
    print("entered loop")
    test3.name = 'Testing uncommited row %s ' % (i,)
    test3.value = 'Uncommited row %s ' % (i,)
    test3.date = datetime.utcnow()
    test3.save(commit=False)
test3.rollback()

print("\n----------- Insert 3, commit!")
test3 = db.model('test','id_test')
for i in range(0,5):
    test3.name = 'Testing commited row %s ' % (i,)
    test3.value = 'Commited row'
    test3.date = datetime.utcnow()
    test3.save()
test3.commit()

print("\n----------- Not clearing the instance, only changes will be applied to the same row")
test4 = db.model('test','id_test')
for i in range(0,3):
    test4.name = 'Testing not clearing at save - change %s ' % (i,)
    test4.value = 'Uncleared row - change %s ' % (i,)
    test4.date = datetime.utcnow()
    test4.save(clear=False)
test4.commit()

print("\n----------- Testing finding one row by multiple attributes")
test5 = db.model('test','id_test')
test5.find_by(name='Modified testing name',value='Testing value')
print(test5.values)
print("\n----------- Testing not finding values by key")
test5 = db.model('test','id_test')
test5.find_by(value='Non existent')
print(test5.values)


print("\n----------- Testing finding multiple row by multiple attributes")
test5.clear()
test5.find_by(value='Commited row')
print(test5.rows)


print("\n----------- Delete last record: %s " % test3.last_id)
test5 = db.model('test','id_test')
test5.id_test = test3.last_id
test5.delete()


db.close()
