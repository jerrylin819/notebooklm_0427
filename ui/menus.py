# 選單對應表（格式、風格等）
MENU_MAIN = """
📚 【NotebookLM 小龍蝦助手】
━━━━━━━━━━━━━━━━━━━━
【筆記本管理】
  1. 建立筆記本
  2. 列出所有筆記本
  3. 切換筆記本
  4. 刪除筆記本

【來源管理】
  5. 新增來源（URL / PDF / YouTube）
  6. 網路研究並自動匯入
  7. 列出來源

【問答】
  8. 向筆記本提問

【生成內容】
  9. 🎙️ 音檔 Podcast
 10. 🎬 影片
 11. 🎬 電影風格影片
 12. 📊 簡報（PDF / PPTX）
 13. 🗺️ 心智圖
 14. 📝 報告
 15. ❓ 測驗
 16. 🃏 學習卡
 17. 📈 資料表
 18. 🖼️ 資訊圖表

【下載】
 19. 下載已生成的內容

【系統】
 20. 查看目前筆記本
 21. 重新登入認證
  0. 離開
━━━━━━━━━━━━━━━━━━━━
"""

MENU_AUDIO = """
🎙️ 【音檔 Podcast 設定】
━━━━━━━━━━━
【格式】
  1. 深度對談（deep-dive）
  2. 簡短摘要（brief）
  3. 批判分析（critique）
  4. 辯論對決（debate）

【長度】
  a. 短（short）
  b. 預設（default）
  c. 長（long）

【語言】
  i.  繁體中文
  ii. 英文
  iii.其他（手動輸入）

請依序輸入：格式 長度 語言
範例：1 b i
"""
MENU_VIDEO = """
🎬 <b>影片設定</b>
━━━━━━━━━━━━━
<b>格式：</b>
  1. 說明影片（explainer）
  2. 簡短摘要（brief）
  3. 電影風格（cinematic）

<b>視覺風格：</b>
  a. 白板（whiteboard）
  b. 動態（animated）
  c. 簡約（minimal）
  d. 企業（corporate）
  e. 教育（educational）
  f. 科技（tech）
  g. 自然（nature）
  h. 復古（retro）
  i. 未來（futuristic）

請依序輸入：格式 風格
範例：1 a
"""

MENU_SLIDE = """
📊 <b>簡報設定</b>
━━━━━━━━━━━━━
<b>格式：</b>
  1. 詳細版（detailed）
  2. 講者版（presenter）

<b>下載格式：</b>
  a. PDF
  b. PPTX（可編輯）

請依序輸入：格式 下載格式
範例：1 b
"""

MENU_INFOGRAPHIC = """
🖼️ <b>資訊圖表設定</b>
━━━━━━━━━━━━━
<b>方向：</b>
  1. 直向（portrait）
  2. 橫向（landscape）
  3. 正方（square）

<b>細節程度：</b>
  a. 簡略（brief）
  b. 標準（standard）
  c. 詳細（detailed）

請依序輸入：方向 細節
範例：1 b
"""

MENU_QUIZ = """
❓ <b>測驗設定</b>
━━━━━━━━━━━━━
<b>數量：</b>
  1. 少（fewer）
  2. 標準（standard）
  3. 多（more）

<b>難度：</b>
  a. 簡單（easy）
  b. 中等（medium）
  c. 困難（hard）

<b>下載格式：</b>
  i.  JSON
  ii. Markdown
  iii.HTML

請依序輸入：數量 難度 格式
範例：2 b i
"""

MENU_FLASHCARD = """
🃏 <b>學習卡設定</b>
━━━━━━━━━━━━━
<b>數量：</b>
  1. 少（fewer）
  2. 標準（standard）
  3. 多（more）

<b>難度：</b>
  a. 簡單（easy）
  b. 中等（medium）
  c. 困難（hard）

<b>下載格式：</b>
  i.  JSON
  ii. Markdown
  iii.HTML

請依序輸入：數量 難度 格式
範例：2 b ii
"""

MENU_REPORT = """
📝 <b>報告設定</b>
━━━━━━━━━━━━━
<b>類型：</b>
  1. 簡報文件（briefing）
  2. 學習指南（study-guide）
  3. 部落格文章（blog-post）
  4. 自訂提示（手動輸入）

請輸入選項：
"""

MENU_DOWNLOAD = """
📥 <b>下載已生成的內容</b>
━━━━━━━━━━━━━
  1. 音檔 Podcast（MP3）
  2. 影片（MP4）
  3. 電影風格影片（MP4）
  4. 簡報 PDF
  5. 簡報 PPTX
  6. 心智圖（JSON）
  7. 報告（Markdown）
  8. 測驗 JSON
  9. 測驗 Markdown
 10. 學習卡 JSON
 11. 學習卡 Markdown
 12. 資料表（CSV）
 13. 資訊圖表（PNG）

請輸入選項：
"""


# ... 其他選單