// 这个js文件瞎jb写的 建议改改用

function post(json, url, noticeRet = false, reload = false) {
    var httpRequest = new XMLHttpRequest();

    httpRequest.open('POST', url, true);
    httpRequest.setRequestHeader("Content-type", "application/json");
    httpRequest.send(JSON.stringify(json));
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var ret = JSON.parse(httpRequest.responseText);
            if (noticeRet) {
                if (ret.status == 1) {
                    notice(ret.data.title, ret.data.content, reload);
                } else {
                    notice(ret.data.title ? ret.data.title : "错误", ret.data.content ? ret.data.content : "未知原因", false);
                }
            }

        }
    };
}

function notice(title, content, reload = false) {
    layui.use('layer', function () {
        var layer = layui.layer;
        layui.use('layer', function () {
            var layer = layui.layer;
            layer.open({
                title: title,
                content: content,
                btn: ['确定'],
                btn1: function () {
                    if (reload) {

                        location.reload();

                    }
                    layer.closeAll(); //疯狂模式，关闭所有层
                }
            });
        });
    });
}
