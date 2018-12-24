#!/usr/bin/python

"""
Author : Amitabh Panda
@copyright reserved

This is the driver script and can be extended further.

"""
import time
import os
import uuid
import logging
from xml.dom import minidom
from flask import Flask, request, render_template


# import user defined packages

from packages.BackEndController import DbTable
from packages.TestScript import TestScripts

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# create a file HANDLER

HANDLER = logging.FileHandler(os.path.basename(__file__) + 'debug.log')
HANDLER.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(formatter)

# add the handlers to the LOGGER
LOGGER.addHandler(HANDLER)

LOGGER.info('Start the web application')

application = Flask(__name__)
application.secret_key = 'test'

# Define basic route and corresponding request HANDLER. The function app-that-works-on-function app.


@application.route('/')
def index():
    try:
        rows = DbTable().fetch_rows()
        return render_template('login.html', rows=rows)
    except Exception as e:
        LOGGER.info('Error on fetching data from database is : %s', e)
        return render_template('login.html')


@application.route('/', methods=['GET', 'POST'])
def post_data():
    """

    :rtype: UI object
    """
    flag_exec = 0
    flag = 0
    if request.method == 'POST':
        save = request.form
        col = [1, 'None', 'None', 0, 'None', 1, 'Not Run']
        col[0] = str(uuid.uuid4().fields[-1])[:5]
        col[2] = time.ctime()
        for key, value in save.iteritems():
            if key == 'Test Template':
                col[4] = value
                print col[4]
            elif key == 'Requester':
                col[1] = value
            elif key == 'Test Environment':
                col[3] = value
            elif key == 'Relative Path':
                testdir = os.getcwd() + '/' + value + '/'
                LOGGER.info('Path of the test execution is : %s', testdir)
                if value == '':
                    # default path=/tests; if nothing is entered in custom path
                    testdir = os.getcwd() + '/tests/'
                    LOGGER.info('Path of the test execution is : %s', testdir)
                    flag_exec = 1
                else:
                    if os.path.isdir(testdir):
                        LOGGER.info('Path of the test execution is : %s', testdir)
                    else:
                        error = "Relative Path is not valid"
                        testdir = value
                        LOGGER.info('Path of the test execution is : %s', testdir)
                        flag = 1
                        LOGGER.info('Path of the test execution is : %s', error)
    if flag_exec == 0 and flag == 1:
        col[4] = "Custom Test Dir-" + col[4] + '  :' + testdir + '     ' + error
        DbTable().insert_table(col)
        return index()

    if flag_exec == 1:
        LOGGER.info('Executing requested tests')
        print col[4]
        TestScripts(testdir).test_script_execution(execution=col[4])
        col[4] = "Custom Test Dir-" + col[4] + '  PATH:  ' + testdir
        LOGGER.info('Inserting table data')
        DbTable().insert_table(col)
        if os.path.isfile(os.getcwd() + "/testresult/Flag"):
            LOGGER.info('Updating table data')
            DbTable().update_table(status='Fail', col_val=col[0])
            os.remove(os.getcwd() + "/testresult/Flag")
        else:
            LOGGER.info('Updating table data')
            DbTable().update_table(status='Completed', col_val=col[0])
    else:
        LOGGER.info('Executing requested tests')
        TestScripts(testdir).test_script_execution()
        col[4] = "Custom Test Dir-" + col[4] + '  PATH:  ' + testdir
        LOGGER.info('Inserting table data')
        DbTable().insert_table(col)
        if os.path.isfile(os.getcwd() + "/testresult/Flag"):
            LOGGER.info('Updating table data')
            DbTable().update_table(status='Fail', col_val=col[0])
            os.remove(os.getcwd() + '/testresult/Flag')
        else:
            LOGGER.info('Updating table data')
            DbTable().update_table(status='Completed', col_val=col[0])

    return index()
    # return render_template('login.html', rows=rows, colour=colour)


@application.route('/log.html')
def display():
    content = open(LOGPATH, "r").readlines()
    return render_template("log.html", content=content)


@application.route('/result.html')
def result():
    content = open(RESULTPATH, "r").readlines()
    dictionary = {}
    for i in content:
        i = i.split(",")
        try:
            dictionary[i[0]] = i[1]
        except Exception as e:
            LOGGER.info('Blank line(s) exists.')
            LOGGER.info('Index Out of Range: %s', e)

    return render_template("result.html", dict=dictionary)

# Execute the main program

if __name__ == '__main__':

    ROOTPATH = os.getcwd() + "/settings.xml"
    HOST = minidom.parse(ROOTPATH).getElementsByTagName('host')[0].attributes['name'].value
    PORT = int(minidom.parse(ROOTPATH).getElementsByTagName('port')[0].attributes['name'].value)
    LOGPATH = minidom.parse(ROOTPATH).getElementsByTagName('log')[0].attributes['name'].value
    RESULTPATH = minidom.parse(ROOTPATH).getElementsByTagName('result')[0].attributes['name'].value
    RESULTPATH = os.getcwd() + "/" + RESULTPATH
    application.run(HOST, PORT, True)


