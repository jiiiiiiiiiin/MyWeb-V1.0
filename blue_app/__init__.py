from flask import Blueprint, request, session, redirect
from exts import db
from models import Apps

app_blue = Blueprint('app', __name__)
app_list = []
app_scheduler_func = []


class AppAttribute:
    Status_Online = "1"
    Status_Offline = '0'



from blue_app import view_blog
from blue_app import view_library
from blue_app import view_cpdaily
from blue_app import view_weibo
from blue_app import view_ncm


def app_register():
    """
    当执行迁移命令的时候需要吧这个函数注释了才行
    :return:
    """
    global app_list
    flag = False
    for app in app_list:
        app_q = Apps.query.filter(Apps.app_id == app.app_id).first()
        if not app_q:  # 如果不存在则注册
            db.session.add(app)
            flag = True
        else:  # 存在，读取数据库app信息
            app_list[app_list.index(app)] = app_q

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
            # 查询app状态
            app_q = Apps.query.filter(Apps.app_url == tmp_app.app_url).first()
            if app_q.app_status == AppAttribute.Status_Offline:
                return redirect("/")
            elif app_q.app_status == AppAttribute.Status_Online:
                pass
            else:
                return redirect('/')

            # 判断权限
            if session.get('user_status') and session.get("user_info").get("authority") <= app_q.app_authority:
                break
            else:
                # 权限不够
                return redirect("/")


