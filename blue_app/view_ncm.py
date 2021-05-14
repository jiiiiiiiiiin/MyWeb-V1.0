from blue_app import app_blue, app_list, AppAttribute, app_scheduler_func
from models import Apps
from flask import render_template, request, session
from exts import UserAttribute, db, generate_ret, scheduler, bark_msg, my_log
from blue_app.app_ncm import utils
from datetime import datetime

this_app = Apps(app_name="网易云",
                app_url="/ncm",
                app_status=AppAttribute.Status_Online,
                app_authority=UserAttribute.Authority_Root,
                app_id="ncm")
app_list.append(this_app)
app_scheduler_func.extend([
    {
        'id': 'ncm_copy_recommend',
        'func': 'blue_app.view_ncm:copy_recommend',  # 路径：job函数名
        'args': None,
        'trigger': {
            'type': 'cron',
            'hour': 8,
            'minute': 5
        }
    }
])


class NcmConfig:
    phone = ''
    password = ''
    debug = False


class NCM(db.Model):
    __tablename__ = "ncm"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    phone = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    createTime = db.Column(db.DateTime, default=datetime.now)
    bark = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<NCM %r,Phone %r>' % (self.user_id, self.phone)


def ncm_log(content):
    my_log(name=this_app.app_name, content=content)


@app_blue.route(this_app.app_url, endpoint=this_app.app_id)
def ncm_index():
    if session.get("user_status"):
        user_id = session.get("user_info").get("userid")
        q = NCM.query.filter(NCM.user_id == user_id).first()
        return render_template("App/ncm/app_ncm.html", user=q)
    return "error"



@app_blue.route(this_app.app_url + '/login', endpoint=this_app.app_id + '_login', methods=['POST'])
def ncm_login():
    if session.get("user_status"):
        user_id = session.get("user_info").get("userid")
        receive = request.json  # 接受的post的json数据
        res_type = receive.get('type')
        if res_type == 'commit' and receive.get("data"):
            q = NCM.query.filter(NCM.user_id == user_id).first()
            username = receive.get('data').get("username")
            password = receive.get('data').get("password")
            bark = receive.get('data').get("bark")
            if q:
                # 修改密码
                q.password = password
                db.session.commit()
                return generate_ret(1, {'title': '通知', 'content': '密码修改成功。'})
            else:
                # 这里需要判断一下密码是不是正确
                tmp_config = NcmConfig()
                tmp_config.phone = username
                tmp_config.password = password
                tmp_config.bark = bark
                ret = utils.copy_recommend_playlist(tmp_config, ncm_log, login_test=True)
                if ret:
                    q = NCM(user_id=user_id, phone=username, password=password, bark=bark)
                    db.session.add(q)
                    db.session.commit()
                    bark_msg(q.bark, "网易云", "account add success.")
                    return generate_ret(1, {'title': '通知', 'content': '设置成功。'})
                else:
                    return generate_ret(0, {'title': '通知', 'content': '错误。'})
    return generate_ret(0, {'title': '通知', 'content': '失败'})


def copy_recommend():
    with scheduler.app.app_context():
        ncm_users = NCM.query.all()

        for ncm_user in ncm_users:
            tmp_config = NcmConfig()
            tmp_config.phone = ncm_user.phone
            tmp_config.password = ncm_user.password
            ret = utils.copy_recommend_playlist(tmp_config, ncm_log)
            if ret:
                bark_msg(ncm_user.bark, "网易云", "copy recommend success.")
            else:
                bark_msg(ncm_user.bark, "网易云", "copy recommend failure.")
