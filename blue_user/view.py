from flask import request, render_template, session, redirect

from exts import generate_ret, generate_psd, UserAttribute
from blue_user import user_blue
from models import User, Apps


@user_blue.route('/', methods=['GET'])
def user():
    if session.get('user_status'):
        return render_template('user/home.html', Apps=Apps.query.all())
    else:
        return redirect('/user/login')


@user_blue.route('/query', methods=['GET'])
def query():
    """
    查询用户信息
    :return:
    """
    if session.get('user_status') and session.get("user_info") and session.get("user_info").get(
            "authority") == UserAttribute.Authority_Root:
        try:
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
        except TypeError:
            return generate_ret(0, extra={"code": 1, "msg": "错误"})
        all_user = User.query.paginate(page, limit, error_out=False).items
        data = []
        for q_user in all_user:
            data.append({"id": q_user.id,
                         "username": q_user.username,
                         "authority": q_user.authority,
                         "createTime": q_user.createTime})
        ret = {
            "code": 0,
            "msg": "",
            "count": User.query.count(),
            "data": data
        }
        return ret
    return generate_ret(0, extra={"code": 1, "msg": "错误"})


@user_blue.route('/login', methods=['GET', 'POST'])
def login():
    """
    登陆
    :return:
    """
    if request.method == 'GET':
        if session.get("user_status"):
            return redirect("/")
        else:
            return render_template('user/login.html')
    else:
        receive = request.json  # 接受的post的json数据
        res_type = receive.get('type')
        if res_type == 'login' and receive.get("data"):
            username = receive.get('data').get("username")
            password = receive.get('data').get("password")
            remember = receive.get('data').get("remember")
            query_user = User.query.filter(User.username == username,
                                           User.password == generate_psd(password)).first()
            if query_user:
                if remember:
                    session.permanent = True
                else:
                    session.permanent = False
                session['user_status'] = 1
                session["user_info"] = {
                    "username": query_user.username,
                    "authority": query_user.authority,
                    "headPhoto": query_user.headPhoto
                }
                return generate_ret(1, {'title': '通知', 'content': '登陆成功！'})
            else:
                return generate_ret(0, {'title': '通知', 'content': '登陆失败！'})
        elif res_type == 'logout':
            session.clear()
            return generate_ret(1, {'title': '通知', 'content': '退出成功！'})

        else:
            return generate_ret(0, {'title': 'error', 'content': '未知原因！'})
