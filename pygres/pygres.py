#-*- coding: utf-8 -*-
import psycopg2
from .errors import PygresError
from .model import Model

class Pygres(object):

    conn = None
    curs = None
    model = Model
    config = None

    def __init__(self, config):
        self.config = config
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
            # Cursor
            self.cur = self.conn.cursor()
        except:
            raise PygresError('Couldnt connect to Postgres','Missing')
            sys.exit()

    def model(self, table, pk, *initial_data,**kwargs):
        return Model(self, table, pk, *initial_data,**kwargs)
