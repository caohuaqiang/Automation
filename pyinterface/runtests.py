# -*- coding: utf-8 -*
import time, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(__file__))
sys.path.append('./interface')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from pyinterface.ForUse import Report_Mail

# 指定测试用例为当前目录下的interface目录
test_dir = '../pyinterface/interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='jf*.py')


if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='曹华强自动化测试报告',
                            description='接口自动化测试报告')
    # runner = unittest.TextTestRunner()
    runner.run(discover)
    fp.close()

    report_dict = '../pyinterface/report/'
    rm = Report_Mail(report_dict)
    rm.send_mail()

