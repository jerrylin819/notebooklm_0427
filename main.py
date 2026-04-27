# 主程式入口

import sys
import threading
from config import validate_config, NOTEBOOKLM_AVAILABLE, TELEGRAM_BOT_TOKEN
from state import load_state
from ui.session import NotebookLMSession
from integrations.telegram import TelegramBot
from integrations.telegram import TelegramBot, tg_send


def main():
    # 驗證設定
    missing = validate_config()
    if not missing['valid']:  # 明確檢查 'valid' 鍵
        print("❌ 請先在 config.py 填入以下必填欄位：")
        for m in missing['missing']:
            print(f"   - {m}")
        print("\n📖 填入方式：")
        print("   1. 編輯 config.py 檔案")
        print("   2. 找到相應的變數並填入真實值")
        print("   3. 儲存檔案後重新執行此程式")
        sys.exit(1)

    
    # 檢查套件
    try:
        from notebooklm import NotebookLMClient
    except ImportError:
        print("❌ notebooklm 套件未安裝，請先安裝：pip install notebooklm-py")
        sys.exit(1)
    
    session = NotebookLMSession()

     # 啟動 Telegram Bot（背景執行）
    if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "your-telegram-bot-token-here":
        try:
            bot = TelegramBot(session)
            tg_thread = threading.Thread(target=bot.run, daemon=True)
            tg_thread.start()
            print("✅ Telegram Bot 已啟動")
        except Exception as e:
            print(f"⚠️  Telegram Bot 啟動失敗：{e}")
    
    # 終端機模式
    print("\n" + "=" * 45)
    print("🦞 NotebookLM 小龍蝦助手 已啟動")
    print("📱 Telegram Bot 背景執行中")
    print("💡 輸入「選單」查看功能")
    print(f"📌 {session.current_notebook_info()}")
    print("=" * 45)

    while True:
        try:
            user_input = input("\n您的指令 >> ").strip()
        
        except (KeyboardInterrupt, EOFError):
            print("\n👋 再見！")
            break

        if not user_input:
            continue

        result = session.process(user_input)
        if result=="EXIT":
            print("\n👋 再見！")
            break
        if result:
            print(result)

if __name__ == "__main__":
    main()