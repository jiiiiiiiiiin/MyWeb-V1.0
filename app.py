from flask import Flask, render_template, session, current_app

import config
from blue_user import user_blue
from blue_app import app_blue, app_register
from exts import db, UserAttribute
from wxRobot.robot import myrobot
from werobot.contrib.flask import make_view



app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(app_blue, url_prefix='/app')
# app.add_url_rule(rule='/robot/',  # WeRoBot 挂载地址
#                  endpoint='werobot',  # Flask 的 endpoint
#                  view_func=make_view(myrobot),
#                  methods=['GET', 'POST'])

db.init_app(app)


@app.route('/')
@app.route('/index/')
def index():
    # 主页
    print(app.url_map)
    return render_template("index.html")


@app.route('/favicon.ico/')
def favicon():
    # 网页图标
    return current_app.send_static_file('favicon.ico')


@app.context_processor
def my_context_processor():
    ret = {
        "webConfig": config.WebConfig,
        "user_info": session.get("user_info"),
        "user_attribute": UserAttribute
    }
    return ret


with app.app_context():
    app_register()


if __name__ == '__main__':
    app.run()
