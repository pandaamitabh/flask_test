import os
import time
from xml.dom import minidom
import logging


class TestScripts(object):

    def __init__(self, testpath):
        self.testpath = testpath
        self.logdir = os.getcwd() + '/logs/'
        self.testscripts = os.listdir(self.testpath)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create a file HANDLER
        self.handler = logging.FileHandler(os.path.basename(__file__) + 'debug.log')
        self.handler.setLevel(logging.INFO)

        # create a logging format
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        # add the handlers to the LOGGER
        self.logger.addHandler(self.handler)

    def test_script_execution(self, execution='all'):

        if execution == 'all':
            for name in self.testscripts:
                pythontest = 'python ' + self.testpath + name + ' > ' + self.logdir + name.split('.')[0] + '_' + time.strftime("%Y%m%d%H%M%S", time.gmtime()) + '.log'
                self.logger.info('Executing python tests: %s ', pythontest)
                os.system(pythontest)
                time.sleep(2)
        else:
            suitepath = os.getcwd() + '/config/' + execution + '.xml'
            tests = minidom.parse(suitepath).getElementsByTagName('test')
            for s in tests:
                pythontest = 'python ' + self.testpath + s.attributes['name'].value + ' > ' + self.logdir + execution + '_' + s.attributes['name'].value.split('.')[0] + '_' + time.strftime("%Y%m%d%H%M%S", time.gmtime()) + '.log'
                self.logger.info('Executing python tests: %s ', pythontest)
                os.system(pythontest)
                time.sleep(2)
