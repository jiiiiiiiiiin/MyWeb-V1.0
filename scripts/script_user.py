from flask_script import Manager
from exts import generate_psd, db
from models import User

user_manager = Manager()


def add_user(username, password, authority):
    query_res = User.query.filter(User.username == username).all()
    if len(query_res) != 0:
        # 判断是否已经注册该用户
        return False
    else:
        tmp_user = User(username=username, password=generate_psd(password), authority=authority)
        db.session.add(tmp_user)
        db.session.commit()
        return True


@user_manager.option('-u', '--username', dest='username')
@user_manager.option('-p', '--password', dest='password')
@user_manager.option('-a', '--authority', dest='authority')
def create(username, password, authority):
    if add_user(username=username, password=password, authority=authority):
        print("Account:{} create success!".format(username, password))
    else:
        print("Account create error!")