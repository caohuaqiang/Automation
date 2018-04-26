# -*- coding: utf-8 -*
import time, sys
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest


test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='jf*.py')


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='caohuaqiangtestreport',
                            description='report for test')
    runner.run(discover)
    fp.close()
