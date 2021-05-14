import time
from pyncm import apis, EapiCryptoRequest, GetCurrentSession, Crypto


@EapiCryptoRequest
def v3_discovery_recommend_songs(device_id, verify_id, os):
    return '/eapi/v3/discovery/recommend/songs', \
           {
               "deviceId": str(device_id),
               "verifyId": str(verify_id),
               "os": str(os),
               "checkToken": Crypto.checkToken()
           }




def copy_recommend_playlist(config, my_log, login_test=False):
    try:
        apis.login.LoginViaCellphone(config.phone, config.password)
    except apis.login.LoginFailedException:
        my_log("{} login failure. [apis.login.LoginFailedException]".format(config.phone))
    login_info = GetCurrentSession().login_info
    if login_info.get("success"):
        my_log("{} login success.".format(config.phone))
        if login_test:
            return True
    else:
        my_log("{} login failure. [{}]".format(config.phone, login_info))
        return False

    recommend_playlist = v3_discovery_recommend_songs('db25c96804ce4f2ee92ce5634bac61b2', 1, 'iOS')
    if recommend_playlist.get("code") != 200:
        my_log("recommend playlist get failure. [{}]".format(recommend_playlist))
        return False
    else:
        my_log("recommend playlist get success.")
    recommend_playlist_dailysongs = recommend_playlist.get("data").get("dailySongs")
    recommend_playlist_dailydongids = []
    for song in recommend_playlist_dailysongs:
        recommend_playlist_dailydongids.append(str(song.get("id")))
    recommend_playlist_dailydongids.reverse()
    recommend_new_playlist_title = time.strftime("%Y-%m-%d", time.localtime()) + " 今日推荐"

    # 新建歌单
    recommend_new_playlist = apis.playlist.SetCreatePlaylist(recommend_new_playlist_title)
    if recommend_new_playlist.get("code") == 200:
        recommend_new_playlist_id = recommend_new_playlist.get("id")
        my_log("new playlist create success, title: {}, id: {}".format(recommend_new_playlist_title,
                                                                       recommend_new_playlist_id))
    else:
        my_log("new playlist create failure. [{}]".format(recommend_new_playlist))
        return False

    # 将今日推荐每首歌添加到新建歌单
    recommend_new_playlist_set = apis.playlist.SetManipulatePlaylistTracks(trackIds=recommend_playlist_dailydongids,
                                                                           playlistId=recommend_new_playlist_id)
    if recommend_new_playlist_set.get("code") == 200:
        my_log("recommend new playlist set success.")
        return True
    else:
        my_log("recommend new playlist set failure. [{}]".format(recommend_new_playlist_set))
        return False


if __name__ == '__main__':
    class Config:
        phone = "18752843353"
        password = "CWcw1157"
        debug = True
    copy_recommend_playlist(config=Config)
    pass
