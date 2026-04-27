# 互動引擎（終端機邏輯）

from ui.menus import (MENU_MAIN, 
                    MENU_AUDIO, 
                    MENU_VIDEO, 
                    MENU_SLIDE,
                    MENU_REPORT,
                    MENU_QUIZ,
                    MENU_FLASHCARD,
                    MENU_INFOGRAPHIC,
                    MENU_DOWNLOAD,
                    )
from ui.maps import AUDIO_FORMAT_MAP, AUDIO_LENGTH_MAP, AUDIO_LANG_MAP
from state import load_state
from api.openai_parser import parse_natural_language
from handlers.notebook import create_notebook, list_notebooks, use_notebook
from handlers.generate import (
    generate_audio, 
    generate_video,
    handle_generate_slide,
    handle_generate_infographic,
    handle_generate_mindmap,
    handle_generate_report,
    handle_generate_quiz,
    handle_generate_flashcard,
    handle_generate_datatable,
    )
from integrations.telegram import tg_send
from handlers.qa import ask_question
from handlers.auth import re_auth, check_auth_status
from handlers.source import add_source, list_sources, research_and_add
from handlers.download import download_artifact

class NotebookLMSession:
    def __init__(self):
        self.state = load_state()
        self.pending_action = None
        self.pending_params = None
        self.sub_menu = None
    
    def current_notebook_info(self) -> str:
        s = load_state()
        return f"📌 目前筆記本：{s['notebook_title']} （{s['notebook_id'] or '未設定'}）"


    def process(self , user_input: str) -> str:
        """主處理邏輯"""

        """
        主處理入口：
        1. 先檢查是否在等待確認
        2. 再檢查是否在子選單
        3. 再做自然語言解析
        4. 最後做選單數字對應
        """

        user_input = user_input.strip()
        if not user_input:
            return "❌ 請輸入指令或選項！"
        
        # 檢查是否在等待確認
        if self.pending_action:
            if user_input.lower() in ["y", "yes", "確定"]:
                action = self.pending_action
                params = self.pending_params
                self.pending_action = None
                self.pending_params = None
                return self._execute_action(action, params)
            else:
                self.pending_action = None
                self.pending_params = None
                return "❌ 已取消操作。"
        

        # 檢查子選單
        if self.sub_menu:
            result = self._handle_sub_menu(user_input)
            return result
        
        # 觸發主選單
        if user_input.lower() in ["notebooklm", "nlm", "選單", "menu"]:
            return MENU_MAIN
        
        # 數字選單快捷
        if user_input.isdigit():
            return self._handle_main_menu(user_input)
        
        # 自然語言解析
        intent = parse_natural_language(user_input)
        action = intent.get("action", "unknown")
        params = intent.get("params", "")

        if action == "unknown":
            return f"🤔 我不確定你的意思，請輸入「選單」查看功能"
        
        if intent.get("confirm_needed"):
            self.pending_action = action
            self.pending_params = params
            return f"⚠️ {intent['confirm_msg']}\n確認請輸入 y，取消請輸入 n"
        
        return self._execute_action(action, params)
    

    def _handle_main_menu(self, choice: str) -> str:
        """處理主選單選項"""
        menu_actions = {
            "1":  ("create",      "請輸入筆記本名稱："),
            "2":  ("list",        ""),
            "3":  ("use",         "請輸入筆記本 ID："),
            "4":  ("delete",      "請輸入要刪除的筆記本 ID（此操作不可復原）："),
            "5":  ("add_source",  "請輸入來源（URL / 檔案路徑 / YouTube 連結）："),
            "6":  ("research",    "請輸入研究主題："),
            "7":  ("list_source", ""),
            "8":  ("ask",         "請輸入問題："),
            "9":  ("audio",       None),  # 進子選單
            "10": ("video",       None),
            "11": ("cinematic",   "請輸入風格描述（留空使用預設）："),
            "12": ("slide",       None),
            "13": ("mindmap",     ""),
            "14": ("report",      None),
            "15": ("quiz",        None),
            "16": ("flashcard",   None),
            "17": ("datatable",   "請輸入資料表描述（例如：比較主要概念）："),
            "18": ("infographic", None),
            "19": ("download",    None),
            "20": ("share_status",""),
            "21": ("share_public",""),
            "22": ("status",      ""),
            "23": ("reauth",      ""),
            "0":  ("exit",        ""),
        }
        if choice not in menu_actions:
            return "❌ 無效選項"
        
        action, prompt = menu_actions[choice]

        # 需要進子選單的項目
        if prompt is None:
            sub_menus = {
                "audio":      MENU_AUDIO,
                "video":      MENU_VIDEO,
                "slide":      MENU_SLIDE,
                "report":     MENU_REPORT,
                "quiz":       MENU_QUIZ,
                "flashcard":  MENU_FLASHCARD,
                "infographic":MENU_INFOGRAPHIC,
                "download":   MENU_DOWNLOAD,
            }
            self.sub_menu = action
            return sub_menus[action].replace("<b>", "").replace("</b>", "")

        # 需要輸入的項目
        if prompt:
            self.sub_menu = f"input:{action}"
            return prompt

        # 直接執行
        return self._execute_action(action, "")

    
    def _handle_sub_menu(self, user_input: str) -> str:
        """處理子選單"""

        menu = self.sub_menu
        # input: 前綴代表等待使用者輸入參數
        if isinstance(menu, str) and menu.startswith("input:"):
            action = menu[6:]
            self.sub_menu = None
            return self._execute_action(action, user_input)
        
        # 子選單選項
        self.sub_menu = None
        return self._execute_action(menu, user_input)
    

    def _execute_action(self, action: str, params: str) -> str:
        """執行指令"""
        if action == "create":
            ok, out = create_notebook(params)
            if not ok and "AUTH_EXPIRED" in out:
                return "🔐 認證已過期，請輸入「23」重新登入後再試"
            if ok:
                self.state = load_state()
                return f"✅ 建立成功！\n{self.current_notebook_info()}"
            return out

        elif action == "list":
            return list_notebooks()

        elif action == "use":
            ok, out = use_notebook(params)
            if ok:
                self.state = load_state()
                return f"✅ 已切換筆記本\n{self.current_notebook_info()}"
            return out

        elif action == "audio":
            return generate_audio(params)
        
        elif action == "video":
            return generate_video(params)
        
        elif action == "cinematic":
            return generate_video(params, cinematic=True)
        
        elif action == "slide":
            return handle_generate_slide(params)
        
        elif action == "infographic":
            return handle_generate_infographic(params)
        
        elif action == "mindmap":
            return handle_generate_mindmap()
        
        elif action == "report":
            return handle_generate_report(params)
        
        elif action == "quiz":
            return handle_generate_quiz(params)
        
        elif action == "flashcard":
            return handle_generate_flashcard(params)
        
        elif action == "datatable":
            return handle_generate_datatable(params)
        
        elif action == "add_source":
            ok, out = add_source(params)
            return out
        
        elif action == "list_source":
            return list_sources()
        
        elif action == "research":
            return research_and_add(params)
        
        elif action == "ask":
            ok, out = ask_question(params)
            return out if ok else out
        
        elif action == "download":
            return download_artifact(params)
        
        elif action == "reauth":
            re_auth()
            return "✅ 重新登入完成"
        
        elif action == "auth_status":
            return check_auth_status()


        elif action == "exit":
            return "EXIT"

        return f"❌ 未知動作：{action}"
    

    


