import sys
sys.path.append('../db_fixture')
from mysql_db import DB

# 创建测试数据
datas = {
    # 发布会表数据
    'sign_event': [{'id': '1', 'nameq': '红米', 'limitq': 2000, 'statusq': 1,
                    'address': '北京会展中心', 'start_time': '2018-04-24 13:46:00', 'create_time': '2018-04-24 13:46:00'},
                   {'id': '5', 'nameq': 'iphone', 'limitq': 100, 'statusq': 1,
                    'address': '上海', 'start_time': '2018-04-24 13:46:00', 'create_time': '2018-04-24 13:46:00'}
                   ],
    # 嘉宾表数据
    'sign_guest': [{'id': 1, 'realname': 'alen1', 'phone': '15821903150', 'email': '342473195@qq.com', 'sign': 0, 'event_id': 1, 'create_time': '2018-04-24 13:46:00'},
                   {'id': 2, 'realname': 'alen2', 'phone': '15821903151', 'email': '342473195@qq.com', 'sign': 0, 'event_id': 1, 'create_time': '2018-04-24 13:46:00'},
                   {'id': 3, 'realname': 'alen3', 'phone': '15821903152', 'email': '342473195@qq.com', 'sign': 0, 'event_id': 5, 'create_time': '2018-04-24 13:46:00'},
                   ],
}


# 将测试数据插入表
def init_data():
    db = DB()
    for table, data in datas.items():
        db.clear(table)
        for d in data:
            db.insert(table, d)
    db.close()


if __name__ == '__main__':
    init_data()