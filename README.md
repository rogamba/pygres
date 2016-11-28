# Pygres
Simple python package for managing postgres database

#### Installation
```shell
$ pip install pygres
```

#### Configuration
Set the configuration variables in a config.py file
```python
SQL_HOST = '127.0.0.1'
SQL_DB = 'demodb'
SQL_USER = 'postgres'
SQL_PASSWORD = ''
SQL_PORT = '5432'
```

Import Db object from Pygres and config
Send configurations to Db object
```python
from pygres import Pygres
config = dict(
    SQL_HOST = '127.0.0.1',
    SQL_DB = 'demo',
    SQL_USER = 'postgres',
    SQL_PASSWORD =  '',
    SQL_PORT="5432",
)
db = Pygres(config)
```
Accesing from another python / flask module
Instantiating an entity and saving data
```python
import db

user = db.model('<table>','<table_pk>')
user.name = "John"
user.last_name = "Smith"
user.age = 25
user.save()

```

#### Editing rows
If you want to edit row, just pass pass the primary key of the row you want to edit and save, set the new values and save
```python
user = db.model('<table>','<table_pk>')
user.id_user = 1
user.name = "Jane"
user.age = 27
user.save()
```

#### Rolling back and committing changes
Changes are auto commited by default while saving, but you can choose not commit an statement and roll it back if necessary:
```python
user = db.model('<table>','<table_pk>')
for i in range(0,3):
    user.name = "User %s " % (i,)
    user.age = 10+i
    user.save(commit=False)

if nothing_happens:
    user.commit()
else:
    user.rollback()
```


#### Querying row
To query a row form the instanced table that returns a dictionary with the format `{ 'column' : 'value', ... }` justo do:
```python
user.get(<id_user>)
user_row = user.values
```

#### Quick querying multiple rows
To execute any sql statement...
```python
q = db.query(
    """
    SELECT * from <table> WHERE <col> = %s
    """,
    (param,)
)
```
To fetch rows as a list of dictionaries if any returned from the executed statement...
```python
rows = q.fetch()
```
The returned variable will be in the format
```python
[
    {   
        'id_row' : 1
        'column1' : 'value',
        'column2' : 'value'
    },
    {   
        'id_row' : 2
        'column1' : 'value',
        'column2' : 'value'
    }
]
```

## Testing

#### Postgres reqs for testing
Prerequisites for testing:
* Install PostgreSQL
* Create database 'demo'
* Create table 'test'
  * id_test     [serial]
  * name        [text]
  * value       [text]
  * date        [timestamp]
