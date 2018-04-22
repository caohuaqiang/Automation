from auto.case.Management import Manage
from auto.method.useful import ini
from pprint import pprint


if __name__ == '__main__':
    config = eval(ini(filepath='./config/borr.ini').get(section='borrow', option='config'))
    pprint(config)
    manage = Manage(config)
    manage.Fa_Biao()
