#!/usr/bin/python
"""

Author : Amitabh Panda
@copyright reserved

backend database connectivity and controller
"""
import sqlite3
import os
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# create a file HANDLER
HANDLER = logging.FileHandler(os.path.basename(__file__) + 'debug.log')
HANDLER.setLevel(logging.INFO)

# create a logging format
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)

# add the handlers to the LOGGER
LOGGER.addHandler(HANDLER)

LOGGER.info('Start developing the web application')


class DbTable(object):

    def get_connection(self):
        conn = sqlite3.connect("TESTDB.db")
        c = conn.cursor()
        return c, conn

    def create_table(self):
        c, conn = self.get_connection()
        try:
            query = 'CREATE TABLE TESTDB1(RequestID INT NOT NULL,Requester TEXT,' \
                   'Created REAL,TestEnvironment INT,Template CHAR(50),TestPlanIDs INT,Status TEXT);'
            LOGGER.info('Create Table')
            c.execute(query)
            conn.commit()
        except Exception as e:
            LOGGER.info('Error on fetching data from database is : %s', e)

    def fetch_rows(self):
        c, conn = self.get_connection()
        query2 = 'SELECT * from TESTDB1'
        try:
            LOGGER.info('Fetch Table Data')
            c.execute(query2)
            rows = c.execute(query2).fetchall()
            rows = list(rows)
            return rows
        except Exception as e:
            LOGGER.info('Error on fetching data from database is : %s', e)
            self.create_table()

    def insert_table(self, col):
        c, conn = self.get_connection()
        col = ','.join(("'" + str(x) + "'") for x in col)
        query1 = 'INSERT INTO TESTDB1(RequestID, Requester, Created, TestEnvironment, ' \
                 'Template, TestPlanIDs, Status) VALUES( ' + col + ');'
        try:
            LOGGER.info('Insert Table Data')
            assert c.execute(query1)
            conn.commit()

        except Exception as e:
            LOGGER.info('Error on fetching data from database is : %s', e)
            self.create_table()

    def update_table(self, status, col_val):
        c, conn = self.get_connection()
        status = "'" + status + "'"
        col_val = "'" + col_val + "'"
        query3 = 'UPDATE TESTDB1 SET Status = ' + status + ' WHERE RequestID = ' + col_val + ';'
        try:
            LOGGER.info('Update Table Data')
            assert c.execute(query3)
            conn.commit()

        except Exception as e:
            LOGGER.info('Error on fetching data from database is : %s', e)
            self.create_table()

    def delete_table(self):
        c, conn = self.get_connection()
        query4 = "DROP TABLE TESTDB1;"
        try:
            LOGGER.info('Delete Table Data')
            c.execute(query4)
            conn.commit()
            conn.close()
        except Exception as e:
            LOGGER.info('Error on fetching data from database is : %s', e)
