# Telegram Bot 相關功能

import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, OUTPUT_DIR
from pathlib import Path


# ==========================================
# Telegram 推播功能
# ==========================================
def tg_send(text: str):
    """推播純文字到 Telegram"""
    if not TELEGRAM_BOT_TOKEN:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
                },
                timeout=10
        )
    except Exception as e:
        print(f"⚠️  Telegram 推播失敗：{repr(e)}")

def tg_send_file(filepath: str , caption: str = ""):
    """推播檔案到 Telegram"""
    if not TELEGRAM_BOT_TOKEN or not Path(filepath).exists():
        return
    
    ext = Path(filepath).suffix.lower()

    try:
        if ext in [".mp3" , ".mp4"]:
            method = "sendAudio" if ext == ".mp3" else "sendVideo"
            with open(filepath , "rb") as f:
                key = "audio" if ext == ".mp3" else "video"
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}",
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
                    files={key: f},
                    timeout=120
                )
        elif ext in [".png", ".jpg"]:
            with open(filepath, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
                    files={"photo": f},
                    timeout=60
                )
        else:
            with open(filepath, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument",
                    data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
                    files={"document": f},
                    timeout=60
                )
    except Exception as e:
        print(f"⚠️  Telegram 檔案推播失敗：{repr(e)}")

class TelegramBot:
    def __init__(self , session):
        self.session = session
        self.offset = 0
    
    def run(self):
        """Telegram Bot 輪詢主迴圈"""
        print("🤖 Telegram Bot 已啟動")
        tg_send("NotebookLM 小龍蝦助手已啟動！")

        while True:
            try:
                response = requests.get(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates",
                    params={"offset": self.offset ,  "timeout": 30},
                    timeout=35
                )
                data = response.json()
                """
                data長這樣：

                {
                "ok": true,
                "result": [
                    {
                    "update_id": 123456789,
                    "message": {
                        "message_id": 1,
                        "from": {
                        "id": 987654321,
                        "first_name": "Jerry"
                        },
                        "chat": {
                        "id": 987654321,
                        "type": "private"
                        },
                        "date": 1710000000,
                        "text": "幫我整理重點"
                    }
                    }
                ]
                }
                """
                
                for update in data.get("result" , []):
                    self.offset = update["update_id"] + 1
                    msg = update.get("message" , {})
                    chat_id = msg.get("chat" , {}).get("id")
                    text = msg.get("text" , "").strip()

                    if chat_id != TELEGRAM_CHAT_ID or not text:
                        continue

                    result = self.session.process(text)

                    if result == "EXIT":
                        tg_send("小龍蝦助手即將關閉，再見！")
                        return
                    if result:
                        tg_send(result)
            except Exception as e:
                print(f"⚠️  Telegram 輪詢錯誤：{repr(e)}")
                time.sleep(5)
                
    def stop(self):
        """停止 Bot"""
        self.running = False