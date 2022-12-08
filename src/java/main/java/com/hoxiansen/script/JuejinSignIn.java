package com.hoxiansen.script;

import cn.hutool.http.HttpRequest;
import cn.hutool.http.HttpResponse;
import cn.hutool.json.JSON;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.hoxiansen.util.NotifyUtil;
import lombok.extern.slf4j.Slf4j;

/**
 * 掘金每日签到：<a href="https://juejin.cn/user/center/signin">掘金每日签到</a>
 */
@Slf4j
public class JuejinSignIn {
    public static void main(String[] args) {
        HttpRequest post = HttpRequest.post("https://api.juejin.cn/growth_api/v1/check_in?aid=2608&uuid=7162434001180722719&spider=0&_signature=_02B4Z6wo00101mDk8UQAAIDD669qpZdPk35g4PXAAPvFpb0nU-..a8U.k5YxPnnYtbg8eaq5DJJIjJAjDB03OFkjn2c.kGMPYLS0GDKY7j4off.p3QqaRed5aRcnetb6yO4bynyObTzJeO3p3a");
        post.header("cookie", "MONITOR_WEB_ID=5413052f-5fbb-442d-b895-dd51c0c3e1ce; _ga=GA1.2.88599347.1667634128; __tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227162434001180722719%2522%252C%2522user_unique_id%2522%253A%25227162434001180722719%2522%252C%2522timestamp%2522%253A1667634127714%257D; passport_csrf_token=1e1f53252046167448ffe55b51ca4c30; passport_csrf_token_default=1e1f53252046167448ffe55b51ca4c30; n_mh=6MSUdoxfW2d1rKkBoKoSeB6gZHOYdKaleztTRNmmRoo; sid_guard=5daf2e3fcab0708b96c52101147328fb%7C1667661086%7C31536000%7CSun%2C+05-Nov-2023+15%3A11%3A26+GMT; uid_tt=32491d3941545a81a5ea010da452a584; uid_tt_ss=32491d3941545a81a5ea010da452a584; sid_tt=5daf2e3fcab0708b96c52101147328fb; sessionid=5daf2e3fcab0708b96c52101147328fb; sessionid_ss=5daf2e3fcab0708b96c52101147328fb; sid_ucp_v1=1.0.0-KDVhZmQ0Yjc4MTJiNTUzYmRkMWMwMjRiOGYwMzViZGY0NDZmODk5OTcKFgi-vJC__fUtEJ76mZsGGLAUOAJA7wcaAmxmIiA1ZGFmMmUzZmNhYjA3MDhiOTZjNTIxMDExNDczMjhmYg; ssid_ucp_v1=1.0.0-KDVhZmQ0Yjc4MTJiNTUzYmRkMWMwMjRiOGYwMzViZGY0NDZmODk5OTcKFgi-vJC__fUtEJ76mZsGGLAUOAJA7wcaAmxmIiA1ZGFmMmUzZmNhYjA3MDhiOTZjNTIxMDExNDczMjhmYg; _tea_utm_cache_2608={%22utm_source%22:%22timeline%22%2C%22utm_medium%22:%22banner%20%22%2C%22utm_campaign%22:%22saleday%22}; _gid=GA1.2.823362494.1670202844");
        post.header("origin", "https://juejin.cn");
        post.header("referer", "https://juejin.cn/");
        post.header("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36");
        post.body("{}");
        try (HttpResponse response = post.execute()) {
            //{"err_no":0,"err_msg":"success","data":{"incr_point":100,"sum_point":571}}
            String body = response.body();
            log.info("body:{}", body);
            JSONObject obj = JSONUtil.parseObj(body);
            Integer err_no = obj.getInt("err_no");
            if (err_no != 0) {
                NotifyUtil.sendNotify("掘金签到失败", body);
                log.error("juejin sign in fail! response:{}", body);
            }
        }
    }
}
