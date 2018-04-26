# -*- coding: utf-8 -*
import requests
import unittest
from pprint import pprint
import os, sys
sys.path.append(os.path.abspath(__file__))
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 父路径-pyinterface
sys.path.insert(0, parentdir)
from pyinterface.db_fixture.pmq import UseDataBase


class Activity(unittest.TestCase):
    """日常活动"""
    def setUp(self):
        self.yuming = 'https://www-t.jfcaifu.com'
        self.session = requests.session()
        self.phone = '17302139300'

    def tearDown(self):
        pass

    def test_login(self):
        session = self.session
        path_login = '/wap/user/doLogin.html'
        response_login = session.request(method='post', params={'mobilePhone': '15821903152', 'pwd': 'a1234567'}, url=self.yuming + path_login)
        if response_login.status_code == 200 and response_login.json()['msg'] == '登录成功！':
            return response_login
        else:
            print(response_login.status_code, response_login.text)
            raise Exception('登录接口请求失败')

    def test_register(self):
        """注册活动"""
        session = self.session
        path_register = '/activity/flying.html'
        path_code = '/wap/user/getActivityCode.html'
        response_code = session.request(method='post', params={'mobilePhone': self.phone}, url=self.yuming + path_code)
        if response_code.status_code == 200:
            print('获取验证码接口:')
            print(response_code.json())
        else:
            print('验证码接口翻车！！！')

        data_login = {'channelCode': '40409',
                      'pwd': 'a1234567',
                      'mobilePhone': self.phone,
                      'code': '888888'}
        response_login = session.request(method='get', url=self.yuming + path_register, params=data_login)
        if response_login.status_code == 200:
            print('注册接口返回json：')
            print(response_login.json())
            with UseDataBase() as cursor:
                _SQL = "select user_id, user_name, pwd, mobile_phone, channel_type from rd_user where mobile_phone = %s" % self.phone
                cursor.execute(_SQL)
                contents = cursor.fetchall()
                # print(contents)
                # for line in contents:
                #     for data in line:
                #         print(data, end='->')
                # print(contents)
                for data in contents:
                    print('注册用户sql信息：')
                    pprint(data)

    @unittest.skip('跳过登录测试')
    def test_loginz(self):
        """登录接口"""
        session = self.session
        path_login = '/wap/user/doLogin.html'
        response_login = session.request(method='post', params={'mobilePhone': '15821903152', 'pwd': 'a1234567'},
                                         url=self.yuming + path_login)
        if response_login.status_code == 200 and response_login.json()['msg'] == '登录成功！':
            pprint(response_login.json())


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Activity("test_login"))
    runner = unittest.TextTestRunner()
    runner.run(suite)