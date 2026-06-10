import requests
import time
import os

BILI_UID = os.getenv("BILI_UID")
SESSDATA = os.getenv("BILI_SESSDATA")
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")

HEADERS = {
    "Cookie": f"SESSDATA={SESSDATA}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_dynamic():
    url = f"https://api.bilibili.com/x/space/dynamic/search?mid={BILI_UID}&ps=1"
    res = requests.get(url, headers=HEADERS)
    data = res.json()
    if data["code"] != 0:
        return None
    return data["data"]["items"][0]

def is_charging_dynamic(item):
    # 充电专属动态会有 "is_only_fans" 标记
    return item.get("is_only_fans", False)

def send_wechat(title, content):
    url = f"https://www.pushplus.plus/send?token={PUSHPLUS_TOKEN}&title={title}&content={content}"
    requests.get(url)

last_id = ""
while True:
    item = get_dynamic()
    if not item:
        time.sleep(60)
        continue
    dynamic_id = item["id_str"]
    if dynamic_id != last_id and is_charging_dynamic(item):
        last_id = dynamic_id
        title = "🔔 B站充电动态更新"
        content = f"UP主：{item['name']}\n标题：{item['title']}\n链接：https://t.bilibili.com/{dynamic_id}"
        send_wechat(title, content)
    time.sleep(60)
