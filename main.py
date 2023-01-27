import sys
import json
from urllib.request import urlopen
from datetime import datetime
from threading import Thread
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

import m3u
import xmltv


config = json.load(open("config.json"))


class UpdateFilesThread(Thread):
    def __init__(self, threadID, name, delay):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        while True:
            try:
                print("更新频道...")

                channel_info_data = json.loads(
                    urlopen(config["channel_info_url"]).read().decode("utf-8")
                )["data"]
                epg_list_data = json.loads(
                    urlopen(config["epg_list_url"]).read().decode("utf-8")
                )["data"]

                try:
                    channel_cache = json.load(open("cache.json"))
                except FileNotFoundError:
                    channel_cache = {}

                # 获取频道图标
                channel_icon = {}
                for channel in channel_info_data:
                    channel_icon[channel["chnCode"]] = channel["bigChnIcon"]

                # 获取频道信息
                m3u_channel_list: list[m3u.Channel] = []
                xmltv_channel_list: list[xmltv.Channel] = []

                for channel in epg_list_data:
                    tvg_logo = channel_icon[channel["chnCode"]]

                    if channel["chnCode"] in channel_cache:
                        m3u8 = channel_cache[channel["chnCode"]]["m3u8"]
                    else:
                        m3u8 = json.loads(
                            urlopen(channel["playUrl"]).read().decode("utf-8")
                        )["u"]
                        channel_cache[channel["chnCode"]] = {
                            "m3u8": m3u8
                        }

                    m3u_channel = m3u.Channel(
                        tvg_id=channel["chnCode"],
                        tvg_name=channel["chnName"],
                        tvg_logo=tvg_logo,
                        group_title="GITV",
                        m3u8=m3u8
                    )

                    m3u_channel_list.append(m3u_channel)

                    programme_title = channel["title"]
                    programme_start = datetime.fromtimestamp(
                        channel["startTime"] / 1000)
                    programme_stop = datetime.fromtimestamp(
                        channel["endTime"] / 1000)

                    xmltv_channel = xmltv.Channel(
                        channel_id=channel["chnCode"],
                        display_name=channel["chnName"],
                        programme_title=programme_title,
                        programme_start=programme_start,
                        programme_stop=programme_stop
                    )

                    xmltv_channel_list.append(xmltv_channel)

                    print(f"频道：{channel['chnName']}")

                # 保存 M3U 文件
                with open("gitv.m3u", "w", encoding="utf-8") as f:
                    f.write(m3u.M3u(m3u_channel_list).generate_text())

                # 保存 XMLTV 文件
                with open("gitv.xml", "w", encoding="utf-8") as f:
                    f.write(xmltv.Xmltv(xmltv_channel_list).generate_text())

                # 保存缓存
                json.dump(channel_cache, open("cache.json", "w"))

                print("更新完成！")

                time.sleep(config["update_interval"])

            except KeyboardInterrupt:
                sys.exit()

            except Exception as e:
                print(e)


class HttpServerThread(Thread):
    def __init__(self, threadID, name, delay):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay

    def run(self):
        server = HTTPServer(
            (config["listen_address"], config["listen_port"]),
            SimpleHTTPRequestHandler
        )
        server.serve_forever()


def main():
    update_files_thread = UpdateFilesThread(1, "UpdateFilesThread", 1)
    http_server_thread = HttpServerThread(2, "HttpServerThread", 2)

    update_files_thread.start()
    http_server_thread.start()

    update_files_thread.join()
    http_server_thread.join()


if __name__ == '__main__':
    main()
