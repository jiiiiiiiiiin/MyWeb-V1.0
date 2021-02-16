from blue_app import app_blue, app_list, AppAttribute
from models import Apps
from flask import render_template
from exts import UserAttribute


this_app = Apps(app_name="个人博客",
                app_url="/blog",
                app_status=AppAttribute.Status_Online,
                app_authority=UserAttribute.Authority_Visitor,
                app_id="blog")
app_list.append(this_app)


@app_blue.route("/blog", endpoint=this_app.app_id)
def blog():
    return render_template("App/blog/md.html")
