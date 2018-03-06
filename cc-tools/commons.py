#! /usr/bin/env python
# coding: utf8
# @Time: 17-12-25
# @Author: yyq

import os
import re
import json
import phash
import hashlib
import requests
import subprocess
from PIL import Image


class ImageHandle(object):
    def __init__(self, filename):
        self.filename = filename

    def __func(self, command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout, stderr

    def download(self, url):
        count, max = 0, 3
        while 1:
            try:
                resp = requests.get(url, timeout=30)
            except Exception as e:
                print("download e:%s" % repr(e))
                break

            count += 1
            if count > max:
                break
            elif not resp:
                continue
            elif resp.status_code != 200:
                continue

            with open(self.filename, "wb") as f:
                f.write(resp.content)
            break

    def upload_file(self, upload_filename):
        buckket, key = "test", "**/**"
        stdout, stderr = self.__func("filemgr --action mput --bucket %s --key %s --file %s" % (
            buckket, key + "/" + upload_filename, self.filename))
        if "success" in stdout:
            return True
        elif "Success" in stdout:
            return True
        elif "SUCCESS" in stdout:
            return True
        else:
            return False

    def upload_dir(self, local_dir):
        buckket, pre = "test", "**/**/"
        stdout, stderr = self.__func(
            "filemgr --action mput --bucket %s --prefix %s --dir %s" % (buckket, pre, local_dir))
        if "success" in stdout:
            return True
        elif "Success" in stdout:
            return True
        elif "SUCCESS" in stdout:
            return True
        else:
            return False

    def get_size(self):
        return int(os.path.getsize(self.filename))

    def get_info(self):
        try:
            p = Image.open(self.filename)
        except Exception as e:
            raise e

        format = str(p.format).lower()
        is_animated = p.is_animated if format == "gif" else False
        return {
            "width": int(p.width),
            "height": int(p.height),
            "size": self.get_size(),
            "format": format,
            "is_animated": is_animated,
        }

    def get_md5(self):
        try:
            _md5 = hashlib.md5()
        except Exception as e:
            raise e

        f = open(self.filename, "rb")
        while 1:
            _chunk = f.read(1024 * 8)
            if not _chunk: break
            _md5.update(_chunk)
        f.close()

        md5_v = _md5.hexdigest()
        if not md5_v:
            err = "err, no md5 value"
        else:
            return md5_v

    def get_phash(self):
        try:
            return phash.imagehash(self.filename)
        except Exception as e:
            raise e

    def transfer_format(self, new_filename):
        command = "ffmpeg -i %s %s -loglevel -8" % (self.filename, new_filename)
        _, err = self.__func(command)
        if err: return err


class VideoHandle(object):
    def __init__(self, filename):
        self.filename = filename

    def __func(self, command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout, stderr

    def get_info(self):
        stdout, stderr = self.__func(
            "ffprobe -v quiet -print_format json -show_format -show_streams %s" % self.filename)
        if stderr:
            print("get_info err:%s" % stderr)
            return

        info = json.loads(stdout.decode("utf8"))
        if not info:
            print("get_info no info")
            return

        size = info["format"]["size"]
        duration = info["format"]["duration"]
        format = str(info["format"]["format_name"]).lower()
        if len(format) > 5: format = "mp4"
        try:
            width = info["streams"][0]["width"]
            height = info["streams"][0]["height"]
        except KeyError:
            width = info["streams"][1]["width"]
            height = info["streams"][1]["height"]

        return {
            "width": int(width),
            "height": int(height),
            "size": int(size),
            "format": format,
            "duration": float(duration),
        }

    def get_phash(self):
        try:
            return phash.videohash(self.filename)
        except Exception as e:
            print(e)

    def m3u8_to_mp4(self, new_filename):
        stdout, stderr = self.__func(
            "ffmpeg -i %s -acodec copy -vcodec copy -bsf:a aac_adtstoasc -f mp4 %s" % (self.filename, new_filename))

    def video_capture(self, image_filename):
        stdout, stderr = self.__func(
            "ffmpeg -i %s -y -f image2 -start_at_zero -vframes 1 %s -loglevel -8" % (self.filename, image_filename))

    def transfer_format(self, new_filename):
        command = "ffmpeg -i %s %s -loglevel -8" % (self.filename, new_filename)
        _, err = self.__func(command)
        if err: return err


class AppHandle(object):
    def __init__(self, url=None, app_id=None, pkg_name=None):
        self.url = url
        self.app_id = app_id
        self.pkg_name = pkg_name

    def __func(self, command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout, stderr

    def get_pkg_name(self, apk_filename):
        # apk_filename: end with ".apk",like "/data/test.apk"
        _, _ = self.__func("wget {} -0 {} -q --timeout=60".format(self.url, apk_filename))

        # get package name by aapt
        aapt_path = "/"
        cmd = "{} dump badging {} |grep package".format(aapt_path, apk_filename)
        r_cmd = os.popen(cmd)
        content = r_cmd.read()
        r_cmd.close()
        if not content:
            return

        pkg_name = re.search(r"package:\sname='(.*?)'", content).groups()[0]
        os.remove(apk_filename)
        return pkg_name

    def get_an_info(self):
        if self.app_id:
            resp = requests.get("http://m5.qq.com/app/getappdetail.htm?appId={}&sceneId=0".format(self.app_id),
                                timeout=30)
        elif self.pkg_name:
            resp = requests.get("http://m5.qq.com/app/getappdetail.htm?pkgName={}&sceneId=0".format(self.pkg_name),
                                timeout=30)
        else:
            print("get_app_info, no params")
            return

        if not resp:
            return
        elif resp.status_code != 200:
            return

        _d = resp.json().get("obj")
        if not _d:
            return
        elif "appInfo" not in _d:
            return
        else:
            return _d.get("appInfo")

    def get_ios_info(self):
        app_id = re.sub(r"[^0-9]{8,11}", "", self.app_id)
        headers = {
            "X-Apple-Store-Front": "143465-19,20 t:native",
            "User-Agent": "AppStore/2.0 iOS/8.4 model/iPhone7,2 build/12H143 (6; dt:106)",
        }
        resp = requests.get(
            "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id={}&cc=cn".format(app_id),
            headers=headers, timeout=30)

        if not resp:
            return
        elif resp.status_code != 200:
            return
        elif resp.headers["content-type"] != "application/json; charset=UTF-8":
            return

        content = resp.json()
        store_data = content.get("storePlatformData")
        if not store_data: return
        product_dv = store_data.get("product-dv-product")
        if not product_dv: return
        r = product_dv.get("results")
        if not r:
            return
        else:
            return r.get("%s" % app_id)


def check_similar(file_1, file_2):
    phash_1, phash_2 = ImageHandle(file_1).get_phash(), ImageHandle(file_2).get_phash()
    if not phash_1 or not phash_2:
        return

    dist = phash.hamming_dist(int(phash_1), int(phash_2))
    # similar sill use 5
    if dist < 5:
        return True
    else:
        return False
