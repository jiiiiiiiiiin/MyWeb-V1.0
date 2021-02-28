from flask import Flask, render_template, session, current_app
import config
import os
import logging
from blue_user import user_blue
from blue_app import app_blue, app_register, app_scheduler_func
from exts import db, UserAttribute, scheduler, bark_root
from wxRobot.robot import myrobot
from werobot.contrib.flask import make_view
from gevent import pywsgi



app = Flask(__name__)
app.config.from_object(config)
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(app_blue, url_prefix='/app')
app.add_url_rule(rule='/robot',  # WeRoBot 挂载地址
                 endpoint='werobot',  # Flask 的 endpoint
                 view_func=make_view(myrobot),
                 methods=['GET', 'POST'])

db.init_app(app)


@app.route('/')
@app.route('/index/')
def index():
    # 主页
    app.logger.info("from index")
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
    app.config['JOBS'].extend(app_scheduler_func)
    app.logger.info(app_scheduler_func)


if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or 1:  # 解决FLASK DEBUG模式定时任务执行两次
    scheduler.init_app(app)
    scheduler.start()
    bark_root("apscheduler start ok.")

if __name__ == '__main__':
    logging.basicConfig(filename='flask.log', level=logging.DEBUG)
    if os.path.exists("server.env"):
        server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
        server.serve_forever()
    else:
        app.run(host="0.0.0.0", port=80)
