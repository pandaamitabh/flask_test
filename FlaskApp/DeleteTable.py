#!/usr/bin/python

"""
Author : Amitabh Panda
@copyright reserved

This is the driver script and can be extended further.

"""

import sqlite3
conn = sqlite3.connect("TESTDB.db")
c = conn.cursor()

def delete_table():

    try:
        query="DROP TABLE TESTDB1;"
        c.execute(query)
        conn.commit()
        conn.close()

    except Exception as e:
        print e

if __name__ == '__main__':
    delete_table()
