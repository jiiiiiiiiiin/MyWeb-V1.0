from flask import request, render_template, session, redirect

import exts
from blue_user import user_blue
from models import User


@user_blue.route('/', methods=['GET'])
def user():
    if session.get('user_status'):
        return render_template('user/home.html')
    else:
        return redirect('/user/login')


@user_blue.route('/login', methods=['GET', 'POST'])
def login():
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
                                           User.password == exts.generate_psd(password)).first()
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
                return exts.generate_ret(1, {'title': '通知', 'content': '登陆成功！'})
            else:
                return exts.generate_ret(0, {'title': '通知', 'content': '登陆失败！'})
        elif res_type == 'logout':
            session.clear()
            return exts.generate_ret(1, {'title': '通知', 'content': '退出成功！'})

        else:
            return exts.generate_ret(0, {'title': 'error', 'content': '未知原因！'})
