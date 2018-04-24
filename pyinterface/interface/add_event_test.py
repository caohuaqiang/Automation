import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-pyinterface
sys.path.insert(0, parentdir)
from db_fixture import ceshi_data

# class AddEventTest(unittest.TestCase):
#     """添加发布会"""
#
if __name__ == '__main__':
    ceshi_data.init_data()