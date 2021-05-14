import requests


class CpDaily:
    def __init__(self, user):
        self.user = user
        self.apis = {
            'login-url': 'http://authserver.njit.edu.cn/authserver/login?display=skip&service=https%3A%2F%2Fnjit.campusphere.net%2Fportal%2Flogin%3Fdisplay%3Dskip',
            'host': 'njit.campusphere.net'
        }
        pass

    # 登陆并返回session
    def get_session(self):
        params = {
            'login_url': self.apis['login-url'],
            'needcaptcha_url': '',
            'captcha_url': '',
            'username': self.user['username'],
            'password': self.user['password']
        }
        cookies = {}
        # 借助上一个项目开放出来的登陆API，模拟登陆
        res = requests.post("http://cranny.top:8080/wisedu-unified-login-api-v1.0/api/login", params)
        cookieStr = str(res.json()['cookies'])
        if cookieStr == 'None':
            return None

        # 解析cookie
        for line in cookieStr.split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        session = requests.session()
        session.cookies = requests.utils.cookiejar_from_dict(cookies)
        return session


    def handler(self, test=False):
        session = self.get_session()
        if session is not None:
            if test:  # 登陆测试 仅用来判断密码是否正确
                # 登陆成功
                return True
            # 开始签到
        else:
            return False

