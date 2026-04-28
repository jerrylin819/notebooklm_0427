# 🦞 NotebookLM 小龍蝦助手

一個功能完整的 **NotebookLM 互動助手**，支持終端機和 Telegram Bot 兩種模式。

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## ✨ **主要功能**

### 📚 **筆記本管理**
- ✅ 建立新筆記本
- ✅ 列出所有筆記本
- ✅ 切換使用中的筆記本
- ✅ 刪除筆記本

### 📄 **來源管理**
- ✅ 新增來源（URL / PDF / YouTube）
- ✅ 網路研究並自動匯入
- ✅ 列出所有來源

### 💬 **問答互動**
- ✅ 向筆記本提問
- ✅ 即時取得答案

### 🎨 **內容生成**
- 🎙️ **音檔 Podcast** - 深度對談、簡短摘要、批判分析、辯論對決
- 🎬 **影片** - 說明影片、簡短摘要、電影風格
- 📊 **簡報** - PDF 或 PPTX 格式
- 🗺️ **心智圖** - JSON 格式
- 📝 **報告** - 簡報文件、學習指南、部落格文章
- ❓ **測驗** - JSON / Markdown / HTML 格式
- 🃏 **學習卡** - JSON / Markdown / HTML 格式
- 🖼️ **資訊圖表** - PNG 格式
- 📈 **資料表** - CSV 格式

### 🤖 **AI 功能**
- 自然語言指令解析（使用 GPT-4o）
- 智能意圖理解
- 自動參數推斷

### 📱 **Telegram Bot**
- 背景執行推播
- 即時檔案傳輸
- 雙向互動

---

## 🚀 **快速開始**

### **前置需求**
- Python 3.8 或更高版本
- 有效的 Google 帳號（用於 NotebookLM）
- Telegram 帳號（選擇性，若要使用 Bot 功能）
- OpenAI API Key（用於自然語言解析）

### **安裝步驟**

#### **1. 克隆或下載專案**
```bash
git clone <repository-url>
cd notebooklm_assistant
```

#### **2. 建立虛擬環境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### **3. 安裝依賴套件**
```bash
pip install -r requirements.txt
```

#### **4. 配置 config.py**

編輯 `config.py` 檔案，填入以下資訊：

```python
# config.py

# 【必填】Telegram Bot Token
TELEGRAM_BOT_TOKEN = "你的_bot_token"

# 【必填】你的 Telegram Chat ID
TELEGRAM_CHAT_ID = 你的_chat_id

# 【必填】OpenAI API Key
OPENAI_API_KEY = "你的_openai_api_key"

# 【可選】下載檔案存放路徑
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "notebooklm_outputs")
```

#### **5. 執行程式**
```bash
python main.py
```

---

## 📖 **配置指南**

### **獲取 Telegram Bot Token**

```
1. 打開 Telegram，搜尋 @BotFather
2. 輸入命令 /newbot
3. 按照提示建立機器人
4. 複製 BotFather 提供的 Token
   格式：1234567890:ABCDEFghijklmnopqrstuvwxyz
5. 貼入 config.py 的 TELEGRAM_BOT_TOKEN
```

### **獲取 Telegram Chat ID**

```
1. 打開 Telegram，搜尋 @userinfobot
2. 傳送任意訊息給它
3. 它會回傳你的資訊，找到 "id: 987654321"
4. 複製這個數字到 config.py 的 TELEGRAM_CHAT_ID
```

### **獲取 OpenAI API Key**

```
1. 前往 https://platform.openai.com/api-keys
2. 登入你的 OpenAI 帳號
3. 點擊「Create new secret key」
4. 複製新生成的 key（格式：sk-proj-abc123...）
5. 貼入 config.py 的 OPENAI_API_KEY
```

### **NotebookLM 初始化**

首次執行時，程式會要求你登入 Google 帳號：

```bash
執行notebooklm login 進行登入
執行 main.py 後即可開始使用
```

---

## 💻 **使用方式**

### **終端機模式**

```bash
notebooklm login 進行登入
python main.py

# 輸入「選單」查看所有功能
您的指令 >> 選單

# 或直接輸入數字選項
您的指令 >> 1     # 建立筆記本
您的指令 >> 2     # 列出筆記本
您的指令 >> 9     # 生成 Podcast
```

### **選單選項**

#### **【筆記本管理】**
| 選項 | 功能 |
|------|------|
| 1 | 建立新筆記本 |
| 2 | 列出所有筆記本 |
| 3 | 切換筆記本 |
| 4 | 刪除筆記本 |

#### **【來源管理】**
| 選項 | 功能 |
|------|------|
| 5 | 新增來源（URL / PDF / YouTube） |
| 6 | 網路研究並自動匯入 |
| 7 | 列出來源 |

#### **【互動】**
| 選項 | 功能 |
|------|------|
| 8 | 提問 |

#### **【內容生成】**
| 選項 | 功能 |
|------|------|
| 9 | 🎙️ 音檔 Podcast |
| 10 | 🎬 影片 |
| 11 | 🎬 電影風格影片 |
| 12 | 📊 簡報 |
| 13 | 🗺️ 心智圖 |
| 14 | 📝 報告 |
| 15 | ❓ 測驗 |
| 16 | 🃏 學習卡 |
| 17 | 📈 資料表 |
| 18 | 🖼️ 資訊圖表 |

#### **【下載】**
| 選項 | 功能 |
|------|------|
| 19 | 下載已生成的內容 |

#### **【系統】**
| 選項 | 功能 |
|------|------|
| 20 | 查看目前筆記本 |
| 21 | 重新登入認證 |
| 0 | 離開 |

### **Telegram Bot 模式**

程式運行後會自動在背景啟動 Telegram Bot。你可以在 Telegram 中與機器人互動：

```
使用者 >> /start
機器人 >> 🦞 NotebookLM 小龍蝦助手已上線！
          輸入「選單」查看功能

使用者 >> 選單
機器人 >> 📚 【NotebookLM 小龍蝦助手】
          【筆記本管理】...

使用者 >> 1
機器人 >> 請輸入筆記本名稱：
```

---

## 📂 **專案結構**

```
notebooklm_assistant/
├── README.md                  # 說明文件（本檔案）
├── requirements.txt           # 依賴套件列表
├── main.py                    # 程式入口
├── config.py                  # 設定檔（需填入 API Keys）
├── state.py                   # 狀態管理
│
├── api/                       # API 互動層
│   ├── __init__.py
│   ├── notebooklm_cli.py      # NotebookLM CLI 包裝器
│   └── openai_parser.py       # 自然語言解析（GPT-4o）
│
├── integrations/              # 外部服務整合
│   ├── __init__.py
│   └── telegram.py            # Telegram Bot 功能
│
├── handlers/                  # 業務邏輯層
│   ├── __init__.py
│   ├── notebook.py            # 筆記本管理
│   ├── source.py              # 來源管理
│   ├── qa.py                  # 問答功能
│   ├── auth.py                # 認證管理
│   ├── download.py            # 檔案下載
│   └── generate.py            # 內容生成
│
├── ui/                        # 使用者介面層
│   ├── __init__.py
│   ├── menus.py               # 選單文字定義
│   ├── session.py             # 互動引擎
│   └── maps.py                # 選單對應表
│
└── utils/                     # 工具函數
    ├── __init__.py
    └── helpers.py             # 共用工具函數
```

---

## 🔧 **常見問題**

### **Q1: 執行時出現 "noebooklm-py 未安裝"**
```bash
# 解決方案
pip install notebooklm-py
```

### **Q2: Telegram Bot 無法接收訊息**
```
檢查清單：
1. ✅ TELEGRAM_BOT_TOKEN 是否正確填入？
2. ✅ TELEGRAM_CHAT_ID 是否正確填入？
3. ✅ 機器人是否在背景運行中？
4. ✅ 確認 Telegram 網路連接正常
```

### **Q3: 生成內容超時**
```
原因：
- 內容生成需要時間（通常 3-10 分鐘）
- 網路連接不穩定
- NotebookLM 伺服器繁忙

解決方案：
- 等待生成完成
- 稍後用「下載」選項取得內容
- 檢查網路連接
```

### **Q4: 認證過期怎麼辦？**
```
步驟：
1. 終端機輸入 23（重新登入）
2. 瀏覽器會自動開啟 Google 登入頁面
3. 完成登入後回到終端機按 Enter
4. 認證完成，可繼續使用
```

---

## 🎯 **使用範例**

### **範例 1：建立筆記本並生成 Podcast**

```bash
python main.py

您的指令 >> 1
請輸入筆記本名稱：Python 學習筆記
✅ 建立成功！

您的指令 >> 5
請輸入來源：https://python.org

您的指令 >> 9
🎙️ 【音檔 Podcast 設定】
  格式：1. 深度對談
  長度：a. 短 b. 預設 c. 長
  語言：i. 繁體中文 ii. 英文

請依序輸入：格式 長度 語言
您的指令 >> 1 b i

🎙️ 開始生成 Podcast...
⏳ 請稍候（約 3~5 分鐘）
✅ 音檔已生成並下載
```

### **範例 2：使用自然語言**

```bash
您的指令 >> 建立一個關於深度學習的筆記本
✅ 建立成功！

您的指令 >> 生成一個電影風格的影片
🎬 開始生成電影風格影片...
✅ 影片已生成並下載

您的指令 >> 我想要一個簡報
📊 開始生成簡報...
✅ 簡報已生成並下載
```

---

## 🔐 **安全建議**

⚠️ **重要：請遵循以下安全措施**

1. **絕不上傳 config.py**
   ```bash
   # 將 config.py 加入 .gitignore
   echo "config.py" >> .gitignore
   ```

2. **使用環境變數（高級用法）**
   ```python
   # 在 config.py 中
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ```

3. **使用備用帳號**
   - 建議使用不重要的 Google 帳號
   - 避免主要帳號被停用

---

## 📊 **效能優化**

### **加快生成速度**

```python
# config.py 中調整
# 減少生成內容的複雜度
# 使用「簡短」而非「詳細」選項
```

### **節省 API 額度**

```
1. 避免重複生成相同內容
2. 使用下載功能重用已生成的內容
3. 在非高峰時段生成
```

---

## 🤝 **貢獻指南**

歡迎提交 Issue 和 Pull Request！

### **開發環境設置**

```bash
# 安裝開發依賴
pip install -r requirements.txt
pip install pytest black flake8

# 執行測試
pytest

# 代碼格式化
black .

# 代碼檢查
flake8
```

---

## 📝 **更新日誌**

### **v1.0.0 (2026-04-27)**
- ✅ 初版發布
- ✅ 支持所有內容生成功能
- ✅ Telegram Bot 整合
- ✅ 自然語言解析
- ✅ 完整的模組化架構

---

## 📄 **授權**

本專案採用 **MIT 授權**。詳見 [LICENSE](LICENSE) 檔案。

---

## ⚖️ **免責聲明**

⚠️ **重要：請在使用前閱讀**

1. 本程式使用非官方第三方套件 `notebooklm-py`
2. 該套件呼叫 Google NotebookLM 的未公開 API
3. 使用者應承擔使用該套件的風險
4. 建議遵守 [Google 服務條款](https://policies.google.com/terms)

---

## 🆘 **取得幫助**

### **常見問題**
- 查看 [常見問題](#-常見問題) 部分

### **提交 Issue**
- 前往 GitHub Issues 頁面


---

## 🌟 **鳴謝**

感謝以下開源專案：
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) - NotebookLM Python API
- [OpenAI](https://openai.com/) - GPT-4o API
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API

---

**祝你使用愉快！🦞**

*最後更新：2026-04-27*
