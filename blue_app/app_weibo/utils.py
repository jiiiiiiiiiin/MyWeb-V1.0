import requests


def get_weibo(uid, containerid=None, userinfo=None):
    if containerid:
        url = "https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}".format(uid, containerid)
    else:
        url = "https://m.weibo.cn/api/container/getIndex?type=uid&value={}".format(uid)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36"
    }
    ret = requests.get(url=url, headers=headers)
    ret = ret.json()
    status = ret.get('ok')
    if status:
        data = ret.get("data")

        if not containerid:
            user_info = data.get('userInfo')
            user_name = user_info.get("screen_name")
            user_img = user_info.get("profile_image_url")
            user_description = user_info.get("description")
            user_info = {
                "username": user_name,
                "description": user_description,
                "image": user_img
            }

            tabs_info = data.get("tabsInfo")
            tabs = tabs_info.get("tabs")
            user_containerid = None
            for tab in tabs:
                if tab.get('title') == "微博":
                    user_containerid = tab.get("containerid")
                    break
            if user_containerid:
                return get_weibo(uid, user_containerid, user_info)
            else:
                return None
        else:
            cards = data.get("cards")
            weibos = []
            for card in cards:
                weibo_url = card.get("scheme")                        # 微博链接
                mblog = card.get("mblog")
                weibo_time = mblog.get("created_at")                  # 时间
                weibo_id = mblog.get("id")                            # id
                weibo_content = mblog.get("text")                     # 内容
                weibo_phone = mblog.get("source")                     # 发布源
                weibo_reposts_count = mblog.get("reposts_count")      # 转发
                weibo_comments_count = mblog.get("comments_count")    # 评论
                weibo_attitudes_count = mblog.get("attitudes_count")  # 点赞
                pic_ids = mblog.get("pic_ids")
                weibo_img = []                                        # 图片
                for pic_id in pic_ids:
                    weibo_img.append("https://wx1.sinaimg.cn/large/{}.jpg".format(pic_id))
                weibo = {
                    "url": weibo_url,
                    "id": weibo_id,
                    "time": weibo_time,
                    "content": weibo_content,
                    "phone": weibo_phone,
                    "reposts": weibo_reposts_count,
                    "comments": weibo_comments_count,
                    "attitudes": weibo_attitudes_count,
                    "image": weibo_img
                }
                weibos.append(weibo)
            data = {
                "userinfo": userinfo,
                "weibos": weibos
            }
            return data

    else:
        return None


if __name__ == '__main__':
    ret = get_weibo("6340252723")
    print(ret)
