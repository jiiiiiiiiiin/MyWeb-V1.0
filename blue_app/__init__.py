from flask import Blueprint
from exts import db
from models import Apps

app_blue = Blueprint('app', __name__)
app_list = []


class AppAttribute:
    Status_Online = 1
    Status_Offline = 0



from blue_app import view_blog


def app_register():
    """
    当执行迁移命令的时候需要吧这个函数注释了才行
    :return:
    """
    global app_list
    for app in app_list:
        if not Apps.query.filter(Apps.app_id == app.app_id).first():
            db.session.add(app)
    db.session.commit()

