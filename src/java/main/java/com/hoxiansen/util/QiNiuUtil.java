package com.hoxiansen.util;

import com.qiniu.common.QiniuException;
import com.qiniu.http.Response;
import com.qiniu.storage.Configuration;
import com.qiniu.storage.Region;
import com.qiniu.storage.UploadManager;
import com.qiniu.util.Auth;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class QiNiuUtil {
    private static final String accessKey = "UkYdVXvBGu3Qoo_iri0wPdEEv3ZTEM3v3ipLYsdF";
    private static final String secretKey = "ojxVAo2BkrBDYebaucACFktUXl0vfg_ijJFx70MG";
    private static final String bucket = "hoxiansen";

    public static boolean upload(byte[] data, String key) {
        Configuration cfg = new Configuration(Region.huadongZheJiang2());
        cfg.resumableUploadAPIVersion = Configuration.ResumableUploadAPIVersion.V2;
        UploadManager uploadManager = new UploadManager(cfg);

        Auth auth = Auth.create(accessKey, secretKey);
        String upToken = auth.uploadToken(bucket);
        Response response = null;
        try {
            response = uploadManager.put(data, key, upToken);
            log.info("upload response:{},key:{}", response, key);
            int statusCode = response.statusCode;
            return statusCode == 200;
        } catch (QiniuException e) {
            log.error("upload error,key{}", key, e);
            return false;
        } finally {
            if (response != null) {
                response.close();
            }
        }
    }
}
