#!/usr/bin/python

"""
Author : Amitabh Panda
@copyright reserved

This is pytest framework and can be extended further.

"""
import os
from xml.dom import minidom
from selenium import webdriver

ROOTPATH = os.getcwd() + "/settings.xml"
HOST = minidom.parse(ROOTPATH).getElementsByTagName('host')[0].attributes['name'].value
PORT = minidom.parse(ROOTPATH).getElementsByTagName('port')[0].attributes['name'].value

drv = webdriver.Chrome()
url = "http://" + HOST + ":" + PORT + "/"


def test_login():
    drv.get(url)
    drv.implicitly_wait(2)
    drv.maximize_window()


def test_id_present():
    assert drv.find_element_by_id("Requester")


def test_fields():
    a = drv.find_element_by_name("Requester").is_enabled()
    if a:
        drv.find_element_by_name("Requester").send_keys("Dev")
        drv.find_element_by_name("Relative Path").send_keys("/tests")
        drv.find_element_by_id("Submit").click()


def test_no_custom_path():
    a = drv.find_element_by_name("Requester").is_enabled()
    if a:
        drv.find_element_by_name("Requester").send_keys("Tester")
        drv.find_element_by_name("Relative Path").send_keys("")
        drv.find_element_by_id("Submit").click()


def test_mandatory():
    drv.find_element_by_name("Relative Path")
	
	
def test_close():
    drv.close()

