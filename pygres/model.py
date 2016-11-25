#-*- coding: utf-8 -*-
import datetime
from psycopg2.extensions import AsIs

class Model(object):
    # db connections
    conn = None
    cur = None
    # global variables
    pk = None
    primary_key = None
    table = None
    columns = None
    rows = None
    qry = None
    primary_key_value = None


    def __init__(self, obj, table, pk, *initial_data,**kwargs):
        # Instantiate the global variables
        self.conn = obj.conn
        self.cur = obj.cur
        # Obtenemos columnas
        self.table = table
        self.primary_key = pk

        self.cur.execute('SELECT * FROM '+ self.table +' LIMIT 0',(self.table,))
        self.columns = [desc[0] for desc in self.cur.description]

        # Alias
        self.cols = self.columns
        self.pk = self.primary_key
        self.pkv = self.primary_key_value

        # If initial_data and kwargs are empty, initialize columns with None value
        for col in self.columns:
            setattr(self, col, None)

        # In case of dictionary initialization
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        # In case of keyworded initialization
        for key in kwargs:
            setattr(self, key, kwargs[key])

    # Standalone query
    def query(self,qry,values):
        self.cur.execute(statement, values)
        self.qry = self.cur.query
        return self

    def run(self):
        pass

    def fetch(self):
        # If we get only one record, new query with the id and instantiate the data
        pass

    '''
    Display the table field values of the current object
    '''
    @property
    def values(self):
        values = {}
        for col in self.columns:
            values[col] = self.__dict__[col]
        return values

    # If the primary key is set, make an update
    def save(self):
        # Insert or update only to the columns that have some value
        ae_fields = []
        for attr, val in self.__dict__.items():
            if attr not in self.columns or val == None:
                continue
            ae_fields.append({
                'column' : attr,
                'value' : val
            })
        print(ae_fields)
        if self.__dict__[self.primary_key] != None and type(self.__dict__[self.primary_key]) == int:
            # Primary key value
            self.pkv =  self.__dict__[self.primary_key]
            # Join the attributes with a comma
            qry_fields = ", ".join([ field['column'] for field in ae_fields ])
            qry_values = ", ".join([ str(field['value']) for field in ae_fields ])
            qry = "UPDATE  %s SET ("+ qry_fields +") = (" + ", ".join([ "%s" for i in range(0,len(ae_fields)) ]) + ") WHERE %s = %s"
        else:
            # Attributes of object intersection with columns
            qry_fields = ", ".join([ field['column'] for field in ae_fields ])
            qry_values = ", ".join([ str(field['value']) for field in ae_fields ])
            qry = "INSERT INTO %s ("+ qry_fields +") VALUES (" + ", ".join([ "%s" for i in range(0,len(ae_fields)) ]) + ")"

        print(qry)
        self.cur.execute(qry, \
            [AsIs(self.table)] + \
            [ str(field['value']) for field in ae_fields ] + \
            ( [AsIs(self.primary_key),AsIs(self.pkv)] if self.pkv else [] ) \
        )
        print(self.cur.query)
        self.conn.commit()
