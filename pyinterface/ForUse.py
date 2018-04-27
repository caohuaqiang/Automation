# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pprint import pprint
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from auto.method.useful import ini
import smtplib
import time
import hashlib
import base64
import requests


class Report_Mail:
    def __init__(self, report_dict):
        self.report_dict = report_dict

    def search_latest_file(self):
        """查找出最新的html文件"""
        lists = os.listdir(self.report_dict)
        lists.sort(key=lambda fn: os.path.getmtime(self.report_dict + fn))
        file_name = lists[-1]
        file_new = os.path.join(self.report_dict, file_name)  # join将报告路径及排序后的最新报告名称合并
        print('file_new: ', file_new)
        print('file_name: ', file_name)
        file_for_deliver = {'file_new': file_new,
                            'file_name': file_name}
        return file_for_deliver

    def send_mail(self):
        """发邮件（附件+正文）"""
        file = self.search_latest_file()
        file_new = file['file_new']
        file_name = file['file_name']
        f = open(file_new, 'rb')
        mail_body = f.read()
        f.close()

        # 邮件正文为测试报告
        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg['Subject'] = Header("自动化测试报告", 'utf-8')

        # 添加附件
        send_file = open(file_new, 'rb').read()
        att = MIMEText(send_file, 'base-64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename = %s' % file_name  # 附件的文件名-在new_report方法中返回可取得

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = Header("曹华强", 'utf-8')  # 邮件主题
        msgRoot.attach(att)
        msgRoot.attach(msg)

        smtp = smtplib.SMTP_SSL()
        smtpsever = "smtp.qq.com"  # 服务器地址
        port = 465
        # 发件人邮箱的账号和密码
        send_user = '342473195@qq.com'
        password = 'nklgzyvjnnxzbggb'
        # 收件人邮箱
        receiver = '342473195@qq.com'
        smtp.connect(host=smtpsever, port=port)
        smtp.login(send_user, password)
        smtp.sendmail(send_user, receiver, msgRoot.as_string())
        smtp.quit()
        print("send email success!")


# def app_sign():
#     """
#     返回data字典：
#     data = {'appkey': ***,
#             'signa': ***,
#              'ts': ***,
#              'id': ***,
#              'pwd': ***}
#     其中，id 和 pwd 取自ini文件夹下的配置文件config.ini的[user]区域的username、password
#     """
#
#     # 加密规则：
#     # 1.appkey = 'V/SQ/yTyYjDmNLXB2unELw==' (死值)
#     # 2.给定一个固定字符串 a = 'LzgvD74cyEspGADEKOxAhA=='
#     # 3.ts 为当前时间的时间戳（中国上海） 10位数字
#     # 4.signa 加密方式为 md5加密  16位小写
#     # 5.pwd 密码  加密方式为  base64加密
#     #
#     # 以下为signa加密方式：
#     # 1.获取到 当前时间的时间戳ts
#     # 2.将给定的固定字符串a与ts拼接得到一个新的字符串，并进行md5加密
#     # 3.将上一步得到的字符串与appkey拼接，得到一个新的字符串，进行md5加密
#     # 4.最后将得到的字符串转为大写，获得到的新字符串即为signa
#
#     appkey = 'V/SQ/yTyYjDmNLXB2unELw=='  # 固定值，得到了appkey
#     a = 'LzgvD74cyEspGADEKOxAhA=='
#
#     ts = int(time.time())
#     # print('ts: ', ts)
#
#     A = a + str(ts)
#     A_md5 = hashlib.md5(A.encode('utf-8'))
#     B = A_md5.hexdigest()  # 按16位输出
#
#     C = B + appkey
#     C_md5 = hashlib.md5(C.encode('utf-8'))
#     D = C_md5.hexdigest()  # 按16位输出
#
#     signa = D.upper()  # 转成大写，得到了signa
#     # print('signa: ', signa)
#
#     filepath = './user.ini'
#     wj = ini(filepath)
#     user = eval(wj.get(section='user', option='chq'))  # 从配置文件中拿到字符串，再转成字典
#
#     phone = user['username']
#     password = user['password']
#     pwd = base64.b64encode(password.encode(encoding='utf-8'))
#
#     # data = {'appkey': appkey,
#     #         'signa': signa,
#     #         'ts': ts,
#     #         'id': phone,
#     #         'pwd': pwd}
#
#     data = {'appkey': appkey,
#             'signa': signa,
#             'ts': ts}
#     return data


# class IOS:
#     def __init__(self, phone, password='a1234567'):
#         """ios签名加密"""
#         appkey = 'V/SQ/yTyYjDmNLXB2unELw=='  # 固定值，得到了appkey
#         a = 'LzgvD74cyEspGADEKOxAhA=='
#         ts = int(time.time())
#         A = a + str(ts)
#         A_md5 = hashlib.md5(A.encode('utf-8'))
#         B = A_md5.hexdigest()  # 按16位输出
#         C = B + appkey
#         C_md5 = hashlib.md5(C.encode('utf-8'))
#         D = C_md5.hexdigest()  # 按16位输出
#         signa = D.upper()  # 转成大写，得到了signa
#         signature = {'appkey': appkey,
#                      'signa': signa,
#                      'ts': ts}
#         self.signature = signature
#         self.phone = phone
#         self.password = password
#         self.session = requests.session()
#
#     def login(self):
#         """登录"""
#         data_login = self.signature
#         data_login['id'] = self.phone
#         data_login['pwd'] = base64.b64encode(self.password.encode(encoding='utf-8'))
#         response = self.session.request(method='post', url='https://www-t.jfcaifu.com/app/user/doLogin.html', params=data_login)


# if __name__ == '__main__':
#     # report_dict = '../pyinterface/report/'
#     # rm = Report_Mail(report_dict)
#     # rm.send_mail()
#
#     # pprint(ios())
#     data = app_sign()
#     print(data)
#
#     session = requests.session()
#     response = session.request(method='post', url='https://www-t.jfcaifu.com/app/user/doLogin.html', params=data)
#     # pprint(response.json())
#
#     token = response.json()['res_data']['oauth_token']
#     # print(token)
#
#     url_index = 'https://www-t.jfcaifu.com/app/v500/index.html'
#     data_index = {'signa': data['signa'], 'ts': data['ts'], 'appkey': app_sign()['appkey'], 'sign': token,}
#     data_index['user_id'] = '1687'
#     response_index = session.request(method='get', url=url_index, params= data_index, )
#     # pprint(response_index.json())
#     pprint(response_index.json()['res_data']['fixBorrowList'])









