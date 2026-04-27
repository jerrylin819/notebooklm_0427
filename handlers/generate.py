# 內容生成（音檔、影片、簡報等）

# handlers/generate.py
"""內容生成模組"""

from datetime import datetime
from api.notebooklm_cli import run_nlm_cli
from state import load_state
from integrations.telegram import tg_send, tg_send_file
from config import OUTPUT_DIR
import os
from ui.maps import (
    AUDIO_FORMAT_MAP, AUDIO_LENGTH_MAP, AUDIO_LANG_MAP,
    VIDEO_FORMAT_MAP, VIDEO_STYLE_MAP,
    SLIDE_FORMAT_MAP, SLIDE_DL_MAP,
    INFOGRAPHIC_ORIENT_MAP, INFOGRAPHIC_DETAIL_MAP,
    QUIZ_QTY_MAP, QUIZ_DIFF_MAP, QUIZ_FMT_MAP,
    REPORT_TYPE_MAP,
)

# ==========================================
# 工具函數
# ==========================================

def _check_notebook() -> tuple[bool, str]:
    """檢查是否選擇了筆記本"""
    state = load_state()
    if not state.get("notebook_id"):
        return False, "❌ 尚未選擇筆記本"
    return True, ""

def _get_timestamp() -> str:
    """取得時間戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _download_file(artifact_type: str, filename: str) -> tuple[bool, str]:
    """下載生成的檔案"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    ok, out = run_nlm_cli("download", artifact_type, filepath)
    return ok, filepath if ok else out

# ==========================================
# 音檔生成
# ==========================================

def handle_generate_audio(params: str) -> str:
    """生成 Podcast"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    parts = params.strip().split()
    fmt = AUDIO_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "deep-dive")
    length = AUDIO_LENGTH_MAP.get(parts[1] if len(parts) > 1 else "b", "default")
    lang_key = parts[2] if len(parts) > 2 else "i"
    lang = AUDIO_LANG_MAP.get(lang_key, lang_key)

    tg_send(f"🎙️ 開始生成 Podcast\n格式：{fmt} | 長度：{length} | 語言：{lang}\n⏳ 請稍候（約 3~5 分鐘）")
    print(f"🎙️ 生成音檔 Podcast：{fmt} / {length} / {lang}")

    try:
        ok, out = run_nlm_cli(
            "generate", "audio",
            "--format", fmt,
            "--length", length,
            "--language", lang,
            timeout=600
        )

        if not ok:
            if "TIMEOUT" in out or out == "TIMEOUT":
                msg = "⏳ 生成中（超過等待時間），請稍後用選項 19 下載"
                tg_send(msg)
                return msg
            return f"❌ 生成失敗：{out}"

        # 自動下載
        ts = _get_timestamp()
        fname = f"podcast_{ts}.mp3"
        ok_dl, fpath = _download_file("audio", fname)
        
        if ok_dl:
            tg_send_file(fpath, caption=f"🎙️ Podcast 完成！\n格式：{fmt} | {lang}")
            return f"✅ 音檔已生成並下載：{fpath}"
        return f"✅ 生成完成，但下載失敗"

    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

# ==========================================
# 影片生成
# ==========================================

def handle_generate_video(params: str, cinematic=False) -> str:
    """生成影片"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    parts = params.strip().split()
    
    if cinematic:
        instructions = params.strip() or "documentary-style summary"
        tg_send(f"🎬 開始生成電影風格影片\n⏳ 請稍候（約 5~10 分鐘）")
        ok, out = run_nlm_cli("generate", "cinematic-video", instructions, timeout=600)
        artifact = "cinematic-video"
    else:
        fmt = VIDEO_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "explainer")
        style = VIDEO_STYLE_MAP.get(parts[1] if len(parts) > 1 else "a", "whiteboard")
        tg_send(f"🎬 開始生成影片\n格式：{fmt} | 風格：{style}\n⏳ 請稍候（約 5~10 分鐘）")
        ok, out = run_nlm_cli("generate", "video", "--format", fmt, "--style", style, timeout=600)
        artifact = "video"

    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            msg = "⏳ 生成中（超過等待時間），請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return f"❌ 生成失敗：{out}"

    ts = _get_timestamp()
    fname = f"video_{ts}.mp4"
    ok_dl, fpath = _download_file(artifact, fname)
    
    if ok_dl:
        tg_send_file(fpath, caption="🎬 影片完成！")
        return f"✅ 影片已生成並下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 簡報生成
# ==========================================

def handle_generate_slide(params: str) -> str:
    """生成簡報"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    parts = params.strip().split()
    fmt = SLIDE_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "detailed")
    dl_fmt = SLIDE_DL_MAP.get(parts[1] if len(parts) > 1 else "b", "pptx")

    tg_send(f"📊 開始生成簡報\n格式：{fmt} | 下載：{dl_fmt.upper()}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "slide-deck", "--format", fmt, timeout=600)
    
    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return f"❌ 生成失敗：{out}"

    ts = _get_timestamp()
    fname = f"slide_{ts}.{dl_fmt}"
    ok_dl, fpath = _download_file("slide-deck", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption=f"📊 簡報完成！（{dl_fmt.upper()}）")
        return f"✅ 簡報已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 資訊圖表生成
# ==========================================

def handle_generate_infographic(params: str) -> str:
    """生成資訊圖表"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    parts = params.strip().split()
    orient = INFOGRAPHIC_ORIENT_MAP.get(parts[0] if len(parts) > 0 else "1", "portrait")
    detail = INFOGRAPHIC_DETAIL_MAP.get(parts[1] if len(parts) > 1 else "b", "standard")

    tg_send(f"🖼️ 開始生成資訊圖表\n方向：{orient} | 細節：{detail}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "infographic", "--orientation", orient, "--detail", detail, timeout=600)
    
    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = _get_timestamp()
    fname = f"infographic_{ts}.png"
    ok_dl, fpath = _download_file("infographic", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption="🖼️ 資訊圖表完成！")
        return f"✅ 資訊圖表已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 心智圖生成
# ==========================================

def handle_generate_mindmap() -> str:
    """生成心智圖"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    tg_send("🗺️ 開始生成心智圖\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "mind-map", timeout=600)
    
    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            return "⏳ 生成中，請稍後用選項 19 下載"
        return out

    ts = _get_timestamp()
    fname = f"mindmap_{ts}.json"
    ok_dl, fpath = _download_file("mind-map", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption="🗺️ 心智圖完成！")
        return f"✅ 心智圖已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 報告生成
# ==========================================

def handle_generate_report(params: str) -> str:
    """生成報告"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    rtype = REPORT_TYPE_MAP.get(params.strip(), None)
    
    if rtype:
        tg_send(f"📝 開始生成報告\n類型：{rtype}\n⏳ 請稍候")
        ok, out = run_nlm_cli("generate", "report", "--format", rtype, timeout=600)
    else:
        tg_send(f"📝 開始生成報告\n⏳ 請稍候")
        ok, out = run_nlm_cli("generate", "report", timeout=600)

    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            return "⏳ 生成中，請稍後用選項 19 下載"
        return out

    ts = _get_timestamp()
    fname = f"report_{ts}.md"
    ok_dl, fpath = _download_file("report", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption="📝 報告完成！")
        return f"✅ 報告已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 測驗生成
# ==========================================

def handle_generate_quiz(params: str) -> str:
    """生成測驗"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    parts = params.strip().split()
    qty = QUIZ_QTY_MAP.get(parts[0] if len(parts) > 0 else "2", "standard")
    diff = QUIZ_DIFF_MAP.get(parts[1] if len(parts) > 1 else "b", "medium")
    fmt = QUIZ_FMT_MAP.get(parts[2] if len(parts) > 2 else "i", "json")

    tg_send(f"❓ 開始生成測驗\n數量：{qty} | 難度：{diff}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "quiz", "--quantity", qty, "--difficulty", diff, timeout=600)
    
    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            return "⏳ 生成中，請稍後用選項 19 下載"
        return out

    ts = _get_timestamp()
    fname = f"quiz_{ts}.{fmt}"
    ok_dl, fpath = _download_file("quiz", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption=f"❓ 測驗完成！（{fmt}）")
        return f"✅ 測驗已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 學習卡生成
# ==========================================

def handle_generate_flashcard(params: str) -> str:
    """生成學習卡"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    parts = params.strip().split()
    qty = QUIZ_QTY_MAP.get(parts[0] if len(parts) > 0 else "2", "standard")
    diff = QUIZ_DIFF_MAP.get(parts[1] if len(parts) > 1 else "b", "medium")
    fmt = QUIZ_FMT_MAP.get(parts[2] if len(parts) > 2 else "i", "json")

    tg_send(f"🃏 開始生成學習卡\n數量：{qty} | 難度：{diff}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "flashcards", "--quantity", qty, "--difficulty", diff, timeout=600)
    
    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            return "⏳ 生成中，請稍後用選項 19 下載"
        return out

    ts = _get_timestamp()
    fname = f"flashcard_{ts}.{fmt}"
    ok_dl, fpath = _download_file("flashcards", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption=f"🃏 學習卡完成！（{fmt}）")
        return f"✅ 學習卡已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"

# ==========================================
# 資料表生成
# ==========================================

def handle_generate_datatable(params: str) -> str:
    """生成資料表"""
    ok, msg = _check_notebook()
    if not ok:
        return msg
    
    prompt = params.strip() or "compare key concepts"
    
    tg_send(f"📈 開始生成資料表\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "data-table", prompt, timeout=600)
    
    if not ok:
        if "TIMEOUT" in out or out == "TIMEOUT":
            return "⏳ 生成中，請稍後用選項 19 下載"
        return out

    ts = _get_timestamp()
    fname = f"datatable_{ts}.csv"
    ok_dl, fpath = _download_file("data-table", fname)
    
    if ok_dl:
        tg_send_file(fpath, caption="📈 資料表完成！")
        return f"✅ 資料表已下載：{fpath}"
    return f"✅ 生成完成，但下載失敗"
