from flask import Blueprint, request, session, redirect
from exts import db
from models import Apps

app_blue = Blueprint('app', __name__)
app_list = []
app_scheduler_func = []


class AppAttribute:
    Status_Online = 1
    Status_Offline = 0



from blue_app import view_blog
from blue_app import view_library


def app_register():
    """
    当执行迁移命令的时候需要吧这个函数注释了才行
    :return:
    """
    global app_list
    flag = False
    for app in app_list:
        if not Apps.query.filter(Apps.app_id == app.app_id).first():
            db.session.add(app)
            flag = True
    if flag:
        db.session.commit()


@app_blue.before_request
def app_filter():
    """
    对用户的权限进行判断并跳转
    :return:
    """
    for tmp_app in app_list:
        if "/app" + tmp_app.app_url in request.path:
            if session.get('user_status') and session.get("user_info").get("authority") <= tmp_app.app_authority:
                break
            else:
                # 权限不够
                return redirect("/")


