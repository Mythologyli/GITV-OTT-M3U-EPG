# GITV OTT M3U EPG

为银河互联网电视（GITV）生成可供 Kodi 使用的 M3U 信号源和 EPG 节目表，支持 HTTP 访问和自动更新。

## 使用方法

1. 通过对 OTT 设备（例如：移动机顶盒）抓包获取 `channel_info_url` 和 `epg_list_url` 两个 URL 并填写在 `config.json` 中。

2. 在 `config.json` 中设置更新时间间隔 `update_interval`，单位为秒。

3. 在 `config.json` 中设置 `listen_address` 和 `listen_port`，用于监听 HTTP 请求。

4. 运行 `python3 main.py`，将会在目录下生成 `gitv.m3u` 和 `gitv.xml`。可以通过访问 `http://<listen_address>:<listen_port>/gitv.m3u` 和 `http://<listen_address>:<listen_port>/gitv.xml` 来获取 M3U 信号源和 EPG 节目表。

5. 通过 Kodi 的 PVR 客户端 PVR IPTV Simple Client 导入 M3U 信号源和 EPG 节目表。建议设置自动更新。

## 注意事项

HTTP 访问利用 `SimpleHTTPRequestHandler` 实现，可以获取到目录下全部文件。因此 `listen_address` 应尽量设置为 `127.0.0.1` 或 `localhost` 以防止安全问题产生。