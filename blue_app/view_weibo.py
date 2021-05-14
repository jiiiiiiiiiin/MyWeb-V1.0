from blue_app import app_blue, app_list, AppAttribute
from models import Apps
from flask import render_template, request, session
from exts import UserAttribute, db
from blue_app.app_weibo import utils
from datetime import datetime

this_app = Apps(app_name="微博",
                app_url="/weibo",
                app_status=AppAttribute.Status_Online,
                app_authority=UserAttribute.Authority_Root,
                app_id="weibo")
app_list.append(this_app)


class WeiBo(db.Model):
    __tablename__ = "weibo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    uid = db.Column(db.Text, nullable=False)
    createTime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<WeiBo %r,UID %r>' % (self.user_id, self.uid)


@app_blue.route(this_app.app_url, endpoint=this_app.app_id)
def weibo_test():
    uid = request.args.get("uid")
    history = None
    if session.get("user_status"):
        user_id = session.get("user_info").get("userid")

        if uid and not WeiBo.query.filter(WeiBo.uid == uid).first():
            tmp_weibo = WeiBo(user_id=user_id, uid=uid)
            db.session.add(tmp_weibo)
            db.session.commit()
        history = WeiBo.query.filter(WeiBo.user_id == user_id).all()

    if uid:
        data = utils.get_weibo(uid)
    else:
        data = None
    return render_template('App/weibo/app_weibo.html', data=data, history=history)
