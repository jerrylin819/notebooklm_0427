#認證管理模組
import os
from api.notebooklm_cli import run_nlm_cli, check_auth
from integrations.telegram import tg_send

# ==========================================
# 認證管理
# ==========================================

def re_auth():
    """重新登入"""
    print("\n🔐 認證已過期，正在重新登入...")
    tg_send("🔐 NotebookLM 認證過期，請在終端機完成重新登入")
    
    storage_dir = os.path.expanduser(os.path.join("~", ".notebooklm"))
    os.makedirs(storage_dir, exist_ok=True)
    
    # 用 os.system 確保完整繼承終端機環境（stdin/stdout/stderr）
    os.system("notebooklm login")
    
    # 驗證是否成功
    if check_auth():
        tg_send("✅ 認證成功！")
        return True
    else:
        tg_send("❌ 認證失敗，請重新嘗試")
        return False

def check_auth_status() -> str:
    """檢查認證狀態"""
    if check_auth():
        return "✅ 認證狀態：有效"
    else:
        return "❌ 認證狀態：已過期，請輸入 23 重新登入"