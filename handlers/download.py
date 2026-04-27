#檔案下載模組
from datetime import datetime
from api.notebooklm_cli import run_nlm_cli
from config import OUTPUT_DIR
from integrations.telegram import tg_send, tg_send_file
import os

# ==========================================
# 下載功能
# ==========================================
DOWNLOAD_MAP = {
    "1":  ("audio",          "podcast_{ts}.mp3",       {}),
    "2":  ("video",          "video_{ts}.mp4",         {}),
    "3":  ("cinematic-video","cinematic_{ts}.mp4",     {}),
    "4":  ("slide-deck",     "slide_{ts}.pdf",         {"format": "pdf"}),
    "5":  ("slide-deck",     "slide_{ts}.pptx",        {"format": "pptx"}),
    "6":  ("mind-map",       "mindmap_{ts}.json",      {}),
    "7":  ("report",         "report_{ts}.md",         {}),
    "8":  ("quiz",           "quiz_{ts}.json",         {"format": "json"}),
    "9":  ("quiz",           "quiz_{ts}.md",           {"format": "markdown"}),
    "10": ("flashcards",     "flashcard_{ts}.json",    {"format": "json"}),
    "11": ("flashcards",     "flashcard_{ts}.md",      {"format": "markdown"}),
    "12": ("data-table",     "datatable_{ts}.csv",     {}),
    "13": ("infographic",    "infographic_{ts}.png",   {}),
}

def download_artifact(choice: str) -> str:
    """下載已生成的內容"""
    if choice not in DOWNLOAD_MAP:
        return "❌ 無效選項"
    
    artifact_type, fname_template, kwargs = DOWNLOAD_MAP[choice]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = fname_template.format(ts=ts)
    filepath = os.path.join(OUTPUT_DIR, fname)
    
    # 構建命令
    args = ["download", artifact_type, filepath]
    for k, v in kwargs.items():
        args += [f"--{k}", v]
    
    ok, out = run_nlm_cli(*args, timeout=120)
    
    if not ok:
        return f"❌ 下載失敗：{out}"
    
    # 推播檔案
    try:
        tg_send_file(filepath, caption=f"📥 {fname}")
    except Exception as e:
        print(f"⚠️  Telegram 推播失敗：{e}")
    
    return f"✅ 下載成功：{filepath}"