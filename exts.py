import hashlib
import json
import requests
import pymysql  # python3.x 没有mysqldb  需要先导入pymysql 在安装mysqldb驱动
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler import events
from datetime import datetime

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


def bark_msg(url, title, content, time_out=1):
    if url[-1] != '/':
        url += '/'
    requests.get("{url}{title}/{content}".format(url=url, title=title, content=content))


def bark_root(content):
    bark_msg("https://api.day.app/DCvStwpdZ6nDfL5Bp4HDzi/", "Server", content)


class UserAttribute:
    Authority_Root = 0
    Authority_User = 1
    Authority_Visitor = 2


pymysql.install_as_MySQLdb()
db = SQLAlchemy()

scheduler = APScheduler()


def event_handle(e):
    job = scheduler.get_job(e.job_id)
    bark_root("event_handle error/missed/max")


scheduler.add_listener(event_handle, mask=(events.EVENT_JOB_ERROR | events.EVENT_JOB_MISSED | events.EVENT_JOB_MAX_INSTANCES))


class MyLog(db.Model):
    __tablename__ = 'mylog'
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    createTime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<log APP:%r>' % self.app_name


def my_log(name, content):
    tmp_log = MyLog(app_name=name, content=content)
    db.session.add(tmp_log)
    db.session.commit()
