import pymysql
from pymysql import connect, cursors
from pymysql.err import OperationalError
import os
import configparser as cparser

# ==================== 读取db_config.ini文件设置========================
base_dir = str(os.path.dirname(os.path.dirname(__file__)))          # 返回 F:/projects/Automation/pyinterface
base_dir = base_dir.replace('\\', '/')
filepath = base_dir + '/db_config.ini'

cf = cparser.ConfigParser()
cf.read(filepath)
db_config = eval(cf.get(section='mysqlconf', option='mysql'))


# =====================封装Mysql基本操作=======================
class DB:
    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(**db_config)
        except OperationalError as err:
            print('Mysql Error %d: %s' % (err.args[0], err.args[1]))

    def clear(self, table_name):
        real_sql = 'DELETE FROM ' + table_name + ';'
        print(real_sql)
        with self.conn.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
            cursor.execute(real_sql)
        self.conn.commit()

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"       # 这个for循环是为了把字典里的value都套上引号，如果没有引号，那么insert的sql语句会报错（insert的values值要引号）
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        sql = 'INSERT INTO ' + table_name + " ("+key+") VALUES ("+value+")"
        print(sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = DB()
    table_name = 'sign_event'
    table_data = {'id': '12',
                  'nameq': '红米',
                  'limitq': 2000,
                  'statusq': 1,
                  'address': '北京会展中心',
                  'start_time': '2018-04-24 13:46:00',
                  'create_time': '2018-04-24 13:46:00'}
    db.clear(table_name)
    db.insert(table_name, table_data)
















