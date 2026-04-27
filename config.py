# 設定檔（API Keys、路徑等）
import os
from pathlib import Path

# ==========================================
# 使用者設定區
# ==========================================

# 【必填】Telegram Bot Token
# 申請方式：在 Telegram 搜尋 @BotFather，輸入 /newbot 依指示建立
TELEGRAM_BOT_TOKEN = "your-telegram-bot-token-here"

# 【必填】你的 Telegram Chat ID
# 取得方式：Telegram 搜尋 @userinfobot，傳任意訊息給它即可看到你的 ID
TELEGRAM_CHAT_ID = 0  # 填入你的 Chat ID

# 【必填】OpenAI API Key（用於自然語言解析）
# 申請方式：https://platform.openai.com/api-keys
OPENAI_API_KEY = "your-openai-api-key-here"

# 【必填】下載檔案存放路徑（建議使用英文路徑，避免中文亂碼）
# 範例：r"C:\Users\你的名字\notebooklm_outputs"
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "notebooklm_outputs")
STORAGE_PATH = os.path.expanduser(r"~\.notebooklm\storage_state.json")
STATE_FILE = os.path.join(OUTPUT_DIR, "nlm_state.json")

# ==========================================
# 【檢查】套件可用性
# ==========================================

NOTEBOOKLM_AVAILABLE = False
try:
    from notebooklm import NotebookLMClient
    NOTEBOOKLM_AVAILABLE = True
except ImportError:
    NOTEBOOKLM_AVAILABLE = False


# ==========================================
# 驗證設定
# ==========================================
def validate_config() -> dict:
    """檢查必填欄位，回傳 {'valid': bool, 'missing': list}"""
    missing = []
    
    # 檢查 Telegram Bot Token
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    elif isinstance(TELEGRAM_BOT_TOKEN, str) and len(TELEGRAM_BOT_TOKEN.strip()) == 0:
        missing.append("TELEGRAM_BOT_TOKEN")
    elif TELEGRAM_BOT_TOKEN == "你的bot_token":
        missing.append("TELEGRAM_BOT_TOKEN")
    
    # 檢查 Telegram Chat ID
    if TELEGRAM_CHAT_ID == 0:
        missing.append("TELEGRAM_CHAT_ID")
    elif not isinstance(TELEGRAM_CHAT_ID, int):
        missing.append("TELEGRAM_CHAT_ID")
    
    # 檢查 OpenAI API Key
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    elif isinstance(OPENAI_API_KEY, str) and len(OPENAI_API_KEY.strip()) == 0:
        missing.append("OPENAI_API_KEY")
    elif OPENAI_API_KEY == "你的openai_key":
        missing.append("OPENAI_API_KEY")
    
    return {
        'valid': len(missing) == 0,
        'missing': missing
    }

# 初始化目錄
os.makedirs(OUTPUT_DIR, exist_ok=True)

