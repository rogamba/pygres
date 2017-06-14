#-*- coding: utf-8 -*-
import datetime
from psycopg2.extensions import AsIs

'''
Pgres table model, references a row in the reference table
and query
'''
class Model(object):
    # db connections
    pygres = None
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
        '''
        obj:    pygres instance containing the db connection and db cursor to query
        table:  table reference from with to query
        pk:     primary key field of the reference table
        pkv:    primary key value
        '''

        # instantiate the object
        self.pygres = obj
        # Instantiate the global variables
        self.conn = obj.conn
        self.cur = obj.cur
        # Obtenemos columnas
        self.table = table
        self.primary_key = pk

        self.cur.execute('SELECT * FROM "' + self.table + '" LIMIT 0',(self.table,))
        self.columns = [desc[0] for desc in self.cur.description]

        # Alias
        self.cols = self.columns
        self.pk = self.primary_key
        self.pkv = self.primary_key_value

        # Query properties
        self.rows = None
        self.result = None
        self.qry = None
        self.query = None

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


    '''
    Display the column names and values of the current object
    '''
    @property
    def values(self):
        values = {}
        for col in self.columns:
            values[col] = self.__dict__[col]
        return values

    # If the primary key is set, make an update
    def save(self,commit=True,clear=True):
        # Insert or update only to the columns that have some value
        ae_fields = []
        for attr, val in self.__dict__.items():
            if attr not in self.columns or val == None:
                continue
            ae_fields.append({
                'column' : attr,
                'value' : val
            })

        # Insert by default, unless a row exists in the db with the same pk value
        qry_fields = ", ".join([ field['column'] for field in ae_fields ])
        qry_values = ", ".join([ str(field['value']) if type(field['value']) != dict else json.dumps(field['value']) for field in ae_fields  ])
        qry = 'INSERT INTO "%s" ('+ qry_fields +') VALUES (' + ', '.join([ '%s' for i in range(0,len(ae_fields)) ]) + ') RETURNING %s'
        # If primary key is set, check if we need to update or insert
        if self.__dict__[self.primary_key] != None:
            # Set primary key value
            self.pkv =  self.__dict__[self.primary_key]
            # Check if record exists in the db
            self.cur.execute('SELECT * FROM "%s" WHERE %s = %s LIMIT 1 ', [AsIs(self.table),AsIs(self.primary_key),self.pkv])
            rc = self.cur.rowcount
            if rc > 0:
                qry = 'UPDATE  "%s" SET ('+ qry_fields +') = (' + ', '.join([ '%s' for i in range(0,len(ae_fields)) ]) + ') WHERE %s = %s RETURNING %s'

        self.cur.execute(qry, \
            [AsIs(self.table)] + \
            [ str(field['value']) if type(field['value']) != dict else json.dumps(field['value']) for field in ae_fields ] + \
            ( [AsIs(self.primary_key),self.pkv] if qry.split(" ")[0] == 'UPDATE' else [] ) + \
            [AsIs(self.primary_key)] \
        )

        self.last_id = self.cur.fetchone()[0]
        setattr(self, self.primary_key, self.last_id)
        setattr(self, 'pkv', self.last_id)
        # If commit parameter is false, do not commit
        if commit:
            self.conn.commit()
        # clear attributes
        if clear:
            self.clear()



    def insert(self,commit=True,clear=True):
        ''' Always insert  in table, must have primary key
        '''
        # Insert or update only to the columns that have some value
        ae_fields = []
        for attr, val in self.__dict__.items():
            if attr not in self.columns or val == None:
                continue
            ae_fields.append({
                'column' : attr,
                'value' : val
            })

        # Generate of not generate primary key value
        qry_fields = ", ".join([ field['column'] for field in ae_fields ])
        qry_values = ", ".join([ str(field['value']) for field in ae_fields ])
        qry = 'INSERT INTO "%s" ('+ qry_fields +') VALUES (' + ', '.join([ '%s' for i in range(0,len(ae_fields)) ]) + ') RETURNING %s'

        self.cur.execute(qry, \
            [AsIs(self.table)] + \
            [ str(field['value']) for field in ae_fields ] + \
            [AsIs(self.primary_key)] \
        )
        self.last_id = self.cur.fetchone()[0]
        setattr(self, self.primary_key, self.last_id)
        setattr(self, 'pkv', self.last_id)
        # If commit parameter is false, do not commit
        if commit:
            self.conn.commit()
        # clear attributes
        if clear:
            self.clear()


    def clear(self):
        ''' Clear column attributes from instance
        '''
        self.pkv = None
        for col in self.columns:
            setattr(self, col, None)

    # Execute commit statement
    def commit(self):
        self.pygres.commit()

    # Rollback changes
    def rollback(self):
        self.pygres.rollback()

    def delete(self,*args):
        '''
        Accept an id of a list of ids to delete
        '''
        # If arguments are sent, delete those
        if args:
            for arg in args:
                if type(arg) == int:
                    ids = [id]
                if type(arg) == list:
                    ids = args
        elif self.__dict__[self.primary_key] != None and type(self.__dict__[self.primary_key]) == int :
            ids = [self.__dict__[self.primary_key]]
        else:
            print("[DELETE] - No arguments were sent ")
            return False

        self.cur.execute(
            """
            DELETE FROM "%s" WHERE %s IN ( """ + ", ".join([ "%s" for i in range(0,len(ids)) ]) + """ )
            """,
            [ AsIs(self.table), AsIs(self.primary_key) ] + \
            ids
        )
        self.clear()
        self.conn.commit()


    def get(self,*args):
        '''
        Get row values, given the id of the row of with the primary
        key value property.
        '''
        if len(args) <= 0:
            if not self.pkv:
                return False
            pkv = self.pkv
        else:
            pkv = args[0]
        rows = self.pygres.query(
            """
            SELECT * FROM "%s" WHERE %s = %s
            """,
            (AsIs(self.table),AsIs(self.primary_key),pkv)
        ).fetch()
        if rows == None or len(rows) <= 0:
            return None
        # Instantiate values
        for k,v in rows[0].items():
            setattr(self,k,v)
        # Return only first row
        return rows[0]


    def find_by(self,**kwargs):
        ''' Get row values, given one or more variables.
            It can only return one row
        '''
        if kwargs is None or len(kwargs) <= 0:
            print("Cannot find row without arguments and values")
            return False
        combined = []
        for key, value in kwargs.items():
            combined.append(AsIs(key))
            combined.append(value)
        # Statement
        rows = self.pygres.query(
            """
            SELECT * FROM "%s" WHERE ("""+  ' AND '.join( [ "%s=%s" for i in range(0,len(kwargs)) ] )  +""")
            """,
            [ AsIs(self.table) ] + \
            combined \
        ).fetch()
        if rows == None or len(rows) <= 0:
            return []

        self.clear()
        self.rows = rows
        if len(rows) > 1:
            ret = rows
        else:
            ret = rows[0]
            # Instantiate values of the first row
            for k,v in rows[0].items():
                setattr(self,k,v)

        # Return only first row
        return ret


    # Query price table
    def select(self,fields="*"):
        self.query['select'] = 'select %s from "%s" ' % (fields, self.table)
        return self

    def where(self,clause):
        self.query['where'] = clause
        return self

    def join(self,clause):
        self.query['join'] = clause
        return self

    def group_by(self,clause):
        self.query['limit'] = clause
        return self

    def order_by(self,clause):
        self.query['order_by'] = clause
        return self

    def run(self):
        '''
        Build SQL query and fetch rows
        '''
        # Build SQL query
        query = self.qry['select'] if 'select' in self.qry and self.qry['select'] != None else 'select * from "%s" ' % self.table
        query += self.qry['join'] if 'join' in self.qry and  self.qry['join'] != None else ""
        query += self.qry['where'] if 'where' in self.qry and self.qry['where'] != None else ""
        query += self.qry['group_by'] if 'group_by' in self.qry and self.qry['group_by'] != None else ""
        query += self.qry['order_by'] if 'order_by' in self.qry and self.qry['order_by'] != None else ""
        query += self.qry['limit'] if 'limit' in self.qry and self.qry['limit'] != None else ""
        self.qry = query

        # Query
        rows = self.pygres.query(self.qry).fetch()
        self.q = self.pygres.q
        self.rows = rows
        return rows

    '''
    Standalone query - just executes a query
    '''
    def query(self,qry,values):
        self.cur.execute(statement, values)
        self.qry = self.cur.query
        return self

    def run(self):
        pass
