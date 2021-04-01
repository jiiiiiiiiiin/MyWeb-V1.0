from blue_app import app_list, app_scheduler_func, AppAttribute, app_blue
from exts import UserAttribute, db, generate_ret
from models import Apps
from datetime import datetime
from flask import request, session

this_app = Apps(app_name="CpDaily",
                app_url="/cpdaily",
                app_status=AppAttribute.Status_Online,
                app_authority=UserAttribute.Authority_User,
                app_id="cpdaily")
app_list.append(this_app)
app_scheduler_func.extend([
    {
        'id': 'sign_am',
        'func': 'blue_app.view_cpdaily:sign',  # 路径：job函数名
        'args': None,
        'trigger': {
            'type': 'cron',
            'hour': 7,
            'minute': 5
        }
    },
    {
        'id': 'sign_pm',
        'func': 'blue_app.view_cpdaily:sign',  # 路径：job函数名
        'args': None,
        'trigger': {
            'type': 'cron',
            'hour': 12,
            'minute': 5
        }
    }
])


class Cpdaily(db.Model):
    __tablename__ = 'cpdaily'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    username = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<cpdaily %r>' % self.username


@app_blue.route(this_app.app_url + '/commit', endpoint=this_app.app_id + '_commit', methods=['POST'])
def commit():
    if session.get("user_status"):
        user_id = session.get("user_info").get("userid")
        receive = request.json  # 接受的post的json数据
        res_type = receive.get('type')
        if res_type == 'commit' and receive.get("data"):
            q = Cpdaily.query.filter(Cpdaily.user_id == user_id).first()
            username = receive.get('data').get("username")
            password = receive.get('data').get("password")
            if q:
                # 修改密码
                q.password = password
                db.session.commit()
                return generate_ret(1, {'title': '通知', 'content': '密码修改成功。'})
            else:
                # 这里需要判断一下密码是不是正确
                q = Cpdaily(user_id=user_id, username=username, password=password)
                db.session.add(q)
                db.session.commit()
                return generate_ret(1, {'title': '通知', 'content': '设置成功。'})
    return generate_ret(0, {'title': '通知', 'content': '失败'})



def sign():
    users = Cpdaily.query.all()
    for user in users:
        # sign
        pass


