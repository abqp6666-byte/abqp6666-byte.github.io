#!/usr/bin/env python3
"""
오늘도 바쁜 AI 사무실 — 로컬 APK 빌드 (Gradle 없이 aapt2/d8/apksigner 직접 호출)

필요한 것:
  JDK 17 (javac, keytool) / Android SDK build-tools 34.0.0 / platform android-34
사용:
  JAVA_HOME=... ANDROID_SDK_ROOT=... python3 tools/build_apk_local.py
결과:
  dist/ai-office-tycoon.apk
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDK = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME") or ""
JDK = os.environ.get("JAVA_HOME") or ""
BT = os.path.join(SDK, "build-tools", "34.0.0")
PLATFORM = os.path.join(SDK, "platforms", "android-34", "android.jar")
PKG = "com.howgrow.aioffice"
NAME = "ai-office-tycoon"
VER_CODE = "4"
VER_NAME = "2.0.1"

BUILD = os.path.join(ROOT, "build", "local")
DIST = os.path.join(ROOT, "dist")


def run(cmd, cwd=None, quiet=False):
    if not quiet:
        print("$", " ".join(cmd[:6]), "..." if len(cmd) > 6 else "")
    r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0:
        print(out[-4000:])
        sys.exit("FAILED: " + " ".join(cmd[:3]))
    if out.strip() and not quiet:
        tail = "\n".join(out.strip().splitlines()[-6:])
        print(tail)
    return out


def main():
    exe = lambda tool: os.path.join(JDK, "bin", tool) if JDK else tool
    javac, keytool = exe("javac"), exe("keytool")
    aapt2 = os.path.join(BT, "aapt2")
    d8 = os.path.join(BT, "d8")
    zipalign = os.path.join(BT, "zipalign")
    apksigner = os.path.join(BT, "apksigner")

    for p in (PLATFORM, aapt2, d8, zipalign, apksigner):
        if not os.path.exists(p):
            sys.exit("없음: " + p)

    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)
    os.makedirs(DIST, exist_ok=True)

    # 0) 게임 원본을 assets 로
    assets = os.path.join(ROOT, "app", "src", "main", "assets", "www")
    os.makedirs(assets, exist_ok=True)
    shutil.copy2(os.path.join(ROOT, "index.html"), os.path.join(assets, "index.html"))

    # 1) javac
    classes = os.path.join(BUILD, "classes")
    os.makedirs(classes)
    srcs = []
    for dp, _, files in os.walk(os.path.join(ROOT, "app", "src", "main", "java")):
        srcs += [os.path.join(dp, f) for f in files if f.endswith(".java")]
    run([javac, "-nowarn", "-source", "17", "-target", "17",
         "-classpath", PLATFORM, "-d", classes] + srcs)

    # 2) d8 → classes.dex
    class_files = []
    for dp, _, files in os.walk(classes):
        class_files += [os.path.join(dp, f) for f in files if f.endswith(".class")]
    dex = os.path.join(BUILD, "dex")
    os.makedirs(dex)
    run([d8, "--lib", PLATFORM, "--min-api", "24", "--output", dex] + class_files)

    # 3) aapt2 compile
    res_zip = os.path.join(BUILD, "res.zip")
    run([aapt2, "compile", "--dir", os.path.join(ROOT, "app", "src", "main", "res"), "-o", res_zip])

    # 4) aapt2 link (manifest 사본에 package 주입)
    man_in = os.path.join(ROOT, "app", "src", "main", "AndroidManifest.xml")
    man = os.path.join(BUILD, "AndroidManifest.xml")
    xml = open(man_in, encoding="utf-8").read()
    xml = re.sub(r'<manifest([^>]*)>',
                 lambda m: '<manifest%s package="%s">' % (m.group(1), PKG)
                 if "package=" not in m.group(1) else m.group(0), xml, count=1)
    open(man, "w", encoding="utf-8").write(xml)

    base_apk = os.path.join(BUILD, "base.apk")
    run([aapt2, "link", "-o", base_apk, "-I", PLATFORM, "--manifest", man,
         "-A", os.path.join(ROOT, "app", "src", "main", "assets"),
         "--min-sdk-version", "24", "--target-sdk-version", "34",
         "--version-code", VER_CODE, "--version-name", VER_NAME,
         "--auto-add-overlay", res_zip])

    # 5) classes.dex 를 APK 루트에 넣기
    with_dex = os.path.join(BUILD, "with_dex.apk")
    shutil.copy2(base_apk, with_dex)
    with zipfile.ZipFile(with_dex, "a", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(dex, "classes.dex"), "classes.dex")

    # 6) zipalign
    aligned = os.path.join(BUILD, "aligned.apk")
    run([zipalign, "-f", "-p", "4", with_dex, aligned])

    # 7) debug keystore + apksigner (키는 저장소에 보관해 서명이 바뀌지 않게 한다)
    ks_src = os.path.join(ROOT, "tools", "debug.keystore")
    ks = os.path.join(BUILD, "debug.keystore")
    if os.path.exists(ks_src):
        shutil.copy2(ks_src, ks)
    if not os.path.exists(ks):
        run([keytool, "-genkeypair", "-v", "-keystore", ks, "-storepass", "android",
             "-alias", "androiddebugkey", "-keypass", "android",
             "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
             "-dname", "CN=Android Debug,O=Android,C=US"])
    out = os.path.join(DIST, NAME + ".apk")
    run([apksigner, "sign", "--ks", ks, "--ks-pass", "pass:android",
         "--key-pass", "pass:android", "--out", out, aligned])
    run([apksigner, "verify", "--print-certs", out])

    size = os.path.getsize(out)
    print("\nOK  %s  (%.1f KB)" % (out, size / 1024.0))


if __name__ == "__main__":
    main()
