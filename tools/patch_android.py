#!/usr/bin/env python3
"""After cap add android, wire the red-R icon and in-app APK installer."""
import os
import shutil
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANDROID = os.path.join(ROOT, "android")
PKG = "com.bwhs.reels"
PKG_PATH = PKG.replace(".", "/")

MAIN = '''package com.bwhs.reels;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.webkit.JavascriptInterface;
import androidx.core.content.FileProvider;
import com.getcapacitor.BridgeActivity;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        attachUpdater();
    }

    @Override
    public void onStart() {
        super.onStart();
        attachUpdater();
    }

    private void attachUpdater() {
        if (getBridge() != null && getBridge().getWebView() != null) {
            getBridge().getWebView().addJavascriptInterface(new Updater(), "BWUpdater");
        }
    }

    private void js(final String code) {
        runOnUiThread(() -> {
            if (getBridge() != null && getBridge().getWebView() != null) {
                getBridge().getWebView().evaluateJavascript(code, null);
            }
        });
    }

    class Updater {
        @JavascriptInterface
        public void downloadAndInstall(final String url) {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && !getPackageManager().canRequestPackageInstalls()) {
                js("window.__bwUpdateStatus&&window.__bwUpdateStatus('Allow install, then tap again')");
                Intent intent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:" + getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
                return;
            }
            new Thread(() -> {
                HttpURLConnection conn = null;
                try {
                    File out = new File(getExternalFilesDir(null), "BWHS-Reels-update.apk");
                    conn = (HttpURLConnection) new URL(url).openConnection();
                    conn.setInstanceFollowRedirects(true);
                    conn.setConnectTimeout(20000);
                    conn.setReadTimeout(120000);
                    conn.connect();
                    int len = conn.getContentLength();
                    InputStream in = conn.getInputStream();
                    FileOutputStream fos = new FileOutputStream(out);
                    byte[] buf = new byte[8192];
                    int n;
                    int got = 0;
                    int last = 0;
                    while ((n = in.read(buf)) != -1) {
                        fos.write(buf, 0, n);
                        got += n;
                        if (len > 0) {
                            int pct = (int) ((got * 100L) / len);
                            if (pct != last) {
                                last = pct;
                                js("window.__bwUpdateProgress&&window.__bwUpdateProgress(" + pct + ")");
                            }
                        }
                    }
                    fos.flush();
                    fos.close();
                    in.close();
                    js("window.__bwUpdateProgress&&window.__bwUpdateProgress(100)");
                    install(out);
                } catch (Exception e) {
                    js("window.__bwUpdateStatus&&window.__bwUpdateStatus('Download failed. Try again')");
                } finally {
                    if (conn != null) conn.disconnect();
                }
            }).start();
        }

        private void install(File apk) {
            runOnUiThread(() -> {
                Uri uri = FileProvider.getUriForFile(MainActivity.this, getPackageName() + ".fileprovider", apk);
                Intent intent = new Intent(Intent.ACTION_VIEW);
                intent.setDataAndType(uri, "application/vnd.android.package-archive");
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(intent);
            });
        }
    }
}
'''

PATHS = '''<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-files-path name="updates" path="." />
    <cache-path name="cache" path="." />
</paths>
'''

def patch_manifest():
    path = os.path.join(ANDROID, "app", "src", "main", "AndroidManifest.xml")
    xml = open(path, encoding="utf-8").read()
    perm = '<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />'
    if perm not in xml:
        xml = xml.replace("<application", perm + "\n    <application", 1)
    provider = '''<provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" />
        </provider>'''
    if "fileprovider" not in xml:
        xml = xml.replace("</application>", "        " + provider + "\n    </application>", 1)
    open(path, "w", encoding="utf-8").write(xml)
    print("manifest patched")

def main():
    java = os.path.join(ANDROID, "app", "src", "main", "java", PKG_PATH, "MainActivity.java")
    os.makedirs(os.path.dirname(java), exist_ok=True)
    open(java, "w", encoding="utf-8").write(MAIN)
    xml_dir = os.path.join(ANDROID, "app", "src", "main", "res", "xml")
    os.makedirs(xml_dir, exist_ok=True)
    open(os.path.join(xml_dir, "file_paths.xml"), "w", encoding="utf-8").write(PATHS)
    patch_manifest()
    icon = os.path.join(ROOT, "icons", "icon-512.png")
    if os.path.exists(icon):
        for folder in glob.glob(os.path.join(ANDROID, "app", "src", "main", "res", "mipmap-*")):
            for name in ("ic_launcher.png", "ic_launcher_round.png", "ic_launcher_foreground.png"):
                shutil.copy(icon, os.path.join(folder, name))
        print("icons copied")

if __name__ == "__main__":
    main()
