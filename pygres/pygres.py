#-*- coding: utf-8 -*-
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .errors import PygresError
from .model import Model

class Pygres(object):

    conn = None
    curs = None
    model = Model
    config = None
    q = None

    def __init__(self, config, **kwargs):
        self.config = config
        # Kwargs
        self.autocommit = kwargs.get('autocommit', False)
        #global conn
        #global cur
        if not self.config:
            raise Pygres("Configuration variables missing",'Missing vars in config')
        # Connection
        try:
            self.conn = psycopg2.connect(
                database=self.config['SQL_DB'],
                user=self.config['SQL_USER'],
                password=self.config['SQL_PASSWORD'],
                host=self.config['SQL_HOST'],
                port=self.config['SQL_PORT']
            )
            # Isolation level, connection with autocommit
            if self.autocommit:
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Cursor
            self.cur = self.conn.cursor()
        except:
            raise PygresError('Couldnt connect to Postgres','Missing')
            sys.exit()

    def close(self):
        self.conn.close()

    def model(self, table, pk, *initial_data,**kwargs):
        return Model(self, table, pk, *initial_data,**kwargs)

    def query(self,statement,values=[],commit=True):
        self.cur.execute(statement, values)
        self.q = self.cur.query
        if commit:
            self.conn.commit()
        return self

    def commit(self):
        self.conn.commit()
        return self

    def rollback(self):
        self.conn.rollback()
        return self

    def fetch(self):
        columns = [desc[0] for desc in self.cur.description]
        rows = self.cur.fetchall()
        rows_list = []
        for row in rows:
            row_dict = {}
            for i,col in enumerate(columns):
                row_dict[col] = row[i]
            rows_list.append(row_dict)
        return rows_list
