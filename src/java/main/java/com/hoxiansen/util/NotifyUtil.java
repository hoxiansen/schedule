package com.hoxiansen.util;

import cn.hutool.core.lang.Assert;
import cn.hutool.http.HttpRequest;
import cn.hutool.http.HttpResponse;
import cn.hutool.http.HttpUtil;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class NotifyUtil {
    public static void sendNotify(String title, String content) {
        sendNotifyByXizhi(title, content);
    }

    private static void sendNotifyByXizhi(String title, String content) {
        Assert.notBlank(title, "param:title can not be blank");
        if (content == null) content = "";
        HttpRequest post = HttpUtil.createPost("https://xizhi.qqoq.net/XZ64b2e3f239e7b355cb82f34cf19dd291.send");
        post.body("title=" + title + "&content=" + content);
        try (HttpResponse response = post.execute()) {
            //{"code":200,"msg":"推送成功"}
            String body = response.body();
            log.info("send notify by xizhi, body:{}", body);
            JSONObject obj = JSONUtil.parseObj(body);
            Integer code = obj.getInt("code");
            if (code != 200) {
                log.error("send notify by xizhi failed.body:{}", body);
            }
        }
    }
}
