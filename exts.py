import hashlib
import json
import requests
import pymysql  # python3.x 没有mysqldb  需要先导入pymysql 在安装mysqldb驱动
from flask_sqlalchemy import SQLAlchemy


def generate_ret(status, data=None, to_str=True, extra=None):
    ret = {
        'status': status,
        'data': data
    }

    if extra:
        ret.update(extra)
    if to_str:
        return json.dumps(ret)
    else:
        return ret


def generate_psd(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode("utf-8"))
    password = sha1.hexdigest()[0:10] + "cwNb"

    sha1.update(password.encode("utf-8"))
    ret = sha1.hexdigest()
    return ret


class UserAttribute:
    Authority_Root = 0
    Authority_User = 1
    Authority_Visitor = 2


pymysql.install_as_MySQLdb()
db = SQLAlchemy()
