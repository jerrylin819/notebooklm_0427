# 狀態管理（儲存和讀取筆記本狀態）

import json
import os
from config import STATE_FILE

def load_state() -> dict:
    """載入目前使用的筆記本狀態"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"notebook_id": None, "notebook_title": "（未設定）"}

def save_state(state: dict):
    """儲存筆記狀態"""
    with open(STATE_FILE, "w" , encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_current_notebook_id() -> str:
    """取得目前使用的筆記本 ID"""
    return load_state().get("notebook_id")

def get_current_notebook_title() -> str:
    """取得目前使用的筆記本標題"""
    return load_state().get("notebook_title", "（未設定）")    