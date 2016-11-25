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

db.close()


# Testeamos nueva instancia del elemento

# Testeamos el borrar el elemento
