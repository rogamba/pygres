from pygres import Pygres

# SQL Alchemy
config = dict(
    SQL_HOST = '127.0.0.1',
    SQL_DB = 'vitamed',
    SQL_USER = 'gamba',
    SQL_PASSWORD =  'Usability',
    SQL_PORT="5432",
)

db = Pygres(config)
price = db.model('price','id_price')
print(price.values)
