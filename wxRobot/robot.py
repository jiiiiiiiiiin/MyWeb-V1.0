from werobot import WeRoBot
from config import WechatConfig


myrobot = WeRoBot(token=WechatConfig.Token)
myrobot.config["APP_ID"] = WechatConfig.AppID
myrobot.config["APP_SECRET"] = WechatConfig.AppSecret

client = myrobot.client

client.create_menu({
    "button": [{
         "type": "click",
         "name": "hha",
         "key": "test_btn"
    }]
})


@myrobot.text
def text(message):
    return "回音墙：{}".format(message.content)


@myrobot.subscribe
def subscribe(message):
    return "谢谢关注!"


@myrobot.key_click("test_btn")
def abort():
    return "啦啦啦，你点击了一个按钮哦"



