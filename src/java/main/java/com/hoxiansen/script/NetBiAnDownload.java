package com.hoxiansen.script;

import cn.hutool.core.util.RandomUtil;
import cn.hutool.core.util.StrUtil;
import cn.hutool.http.HttpRequest;
import cn.hutool.http.HttpUtil;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import com.hoxiansen.util.NotifyUtil;
import com.hoxiansen.util.QiNiuUtil;
import lombok.extern.slf4j.Slf4j;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.ByteArrayOutputStream;

@Slf4j
public class NetBiAnDownload {
    public static void main(String[] args) {
        String html = HttpUtil.get("https://pic.netbian.com/");
        Document document = Jsoup.parse(html);
        Elements uls = document.getElementsByTag("ul");
        Element ul = getSpecificUl(uls);
        if (ul == null) {
            log.error("parse document error, cannot find 'ul.clearfix' element.html:\n{}", html);
            NotifyUtil.sendNotify("彼岸图网下载", "解析html文件失败，未找到ul.clearfix元素");
            return;
        }
        Elements lis = ul.getElementsByTag("li");
        Element li = lis.get(0);
        Elements a = li.getElementsByTag("a");
        String href = a.attr("href");
        String title = a.attr("title");
        // /tupian/31013.html
        String id = StrUtil.subBetween(href, "/tupian/", ".html");
        HttpRequest get = HttpUtil.createGet("https://pic.netbian.com/e/extend/downpic.php?id=" + id + "&t=" + RandomUtil.randomDouble());
        get.cookie("__yjs_duid=1_6e7a6f6dfa8100dca4940dae08cb23c11674982159706; PHPSESSID=41h6nvprdath6212uclu7see91; zkhanmlusername=qq_%BF%C9%BB%D8%CA%D5%C0%AC%BB%F8; zkhanmluserid=6776572; zkhanmlgroupid=1; zkhanmlrnd=kenhACO5IypK7n3Ttc5Q; zkhanmlauth=d5763c10860dc6ddfb6c13362e6eee65; zkhanecookieclassrecord=%2C72%2C53%2C54%2C55%2C66%2C62%2C58%2C59%2C65%2C68%2C63%2C60%2C");
        String resp = get.execute().body();
        log.info("get download url resp:{}", resp);
        JSONObject obj = JSONUtil.parseObj(resp);
        Integer msg = obj.getInt("msg");
        if (msg != 4) {
            // 0：未登录 1：下载量已用完 2：已下载20张 3：3秒后继续下载 5：1台电脑只能下载1张
            log.error("get download url invalid status:({}),resp:{}", msg, resp);
            NotifyUtil.sendNotify("彼岸图网下载", "获取下载链接失败:" + msg);
            return;
        }
        String pic = obj.getStr("pic");
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        HttpUtil.download("https://pic.netbian.com" + pic, out, false);
        byte[] data = out.toByteArray();
        String key = "wallpapers/" + title.replace(" ", "_") + ".jpg";
        boolean uploadSuccess = QiNiuUtil.upload(data, key);
        if (!uploadSuccess) {
            log.error("upload fail.key:{}", key);
            NotifyUtil.sendNotify("彼岸图网下载", "文件上传失败");
        }

    }

    private static Element getSpecificUl(Elements uls) {
        for (Element element : uls) {
            if (element.hasClass("clearfix")) {
                return element;
            }
        }
        return null;
    }
}
