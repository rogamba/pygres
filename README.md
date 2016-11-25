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

user = db.Model('<table>','<table_pk>')
user.name = "John"
user.last_name = "Smith"
user.age = 25
user.save()

```

#### Editing rows
If you want to edit row, just pass pass the primary key of the row you want to edit and save, set the new values and save
```python
user = db.Model('<table>','<table_pk>')
user.id_user = 1
user.name = "Jane"
user.age = 27
user.save()
```
