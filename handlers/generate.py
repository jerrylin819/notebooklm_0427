# 內容生成（音檔、影片、簡報等）

from datetime import datetime
from api.notebooklm_cli import run_nlm_cli
from state import load_state
from integrations.telegram import tg_send, tg_send_file
from config import OUTPUT_DIR
import os
from ui.maps import (
    AUDIO_FORMAT_MAP,
    AUDIO_LENGTH_MAP,
    AUDIO_LANG_MAP,
    VIDEO_FORMAT_MAP,
    VIDEO_STYLE_MAP,
    SLIDE_FORMAT_MAP,
    SLIDE_DL_MAP,
    INFOGRAPHIC_ORIENT_MAP,
    INFOGRAPHIC_DETAIL_MAP,
    QUIZ_QTY_MAP,
    QUIZ_DIFF_MAP,
    QUIZ_FMT_MAP,
    REPORT_TYPE_MAP,
)


# ==========================================
# 音檔生成
# ==========================================
def generate_audio(params: str) -> str:
    """生成 Podcast"""
    parts = params.strip().split()
    fmt = AUDIO_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "deep-dive")
    length = AUDIO_LENGTH_MAP.get(parts[1] if len(parts) > 1 else "b", "default")
    lang_key = parts[2] if len(parts) > 2 else "i"
    lang = AUDIO_LANG_MAP.get(lang_key, lang_key)  # 若非預設則當作自訂語言
    
    tg_send(f"🎙️ 開始生成 Podcast：格式={fmt} 長度={length} 語言={lang}")
    print(f"🎙️ 生成音檔 Podcast：{fmt} / {length} / {lang}")
    args = [f"--format", fmt, "--length", length, "--language", lang]
    ok, out = run_nlm_cli("audio", *args)
    if not ok:
        if out == "TIMEOUT":
            return "⏳ 生成中（超過等待時間），請稍後用選項 19 下載"
        return out
    
    # 自動下載
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"podcast_{ts}.mp3"
    filepath = os.path.join(OUTPUT_DIR , fname)
    ok_dl, out_dl = run_nlm_cli("download", "audio", filepath)

    if ok_dl:
        tg_send_file(filepath, caption=f"🎉 Podcast 生成完成！格式={fmt} 長度={length} 語言={lang}")
        return f"✅ Podcast 生成完成並下載到：{filepath}"

    return f"✅ Podcast 生成完成！但下載失敗"


# ==========================================
# 影片生成
# ==========================================
def generate_video(params: str , cinematic=False) -> str:
    """生成影片"""
    parts = params.strip().split()
    if cinematic:
        instructions = params.strip() or "documentary-style summary"
        tg_send(f"🎬 開始生成電影風格影片...\n⏳ 請稍候（約 5~10 分鐘）")
        ok, out = run_nlm_cli("generate", "cinematic-video", instructions, "--wait", timeout=600)
        artifact = "cinematic-video"
    else:
        fmt = VIDEO_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "explainer")
        style = VIDEO_STYLE_MAP.get(parts[1] if len(parts) > 1 else "a", "whiteboard")
        tg_send(f"🎬 開始生成影片...\n格式：{fmt} | 風格：{style}\n⏳ 請稍候（約 5~10 分鐘）")
        print(f"🎬 生成影片：{fmt} / {style}")
        ok, out = run_nlm_cli("generate", "video", "--format", fmt, "--style", style, "--wait", timeout=600)
        artifact = "video"

    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中（超過等待時間），請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"video_{ts}.mp4"
    filepath = os.path.join(OUTPUT_DIR, fname)
    ok_dl, out_dl = run_nlm_cli("download", artifact, filepath)


    if ok_dl:
        tg_send_file(filepath, caption=f"🎉 影片生成完成！格式={fmt} 風格={style}")
        return f"✅ 影片生成完成並下載到：{filepath}"
    
    return f"✅ 影片生成完成！但下載失敗"

# ==========================================
# 影片生成
# ==========================================
def handle_generate_video(params: str, cinematic=False) -> str:
    """生成影片"""
    parts = params.strip().split()
    
    if cinematic:
        instructions = params.strip() or "documentary-style summary"
        tg_send(f"🎬 開始生成電影風格影片...\n⏳ 請稍候（約 5~10 分鐘）")
        ok, out = run_nlm_cli("generate", "cinematic-video", instructions, "--wait", timeout=600)
        artifact = "cinematic-video"
    else:
        fmt = VIDEO_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "explainer")
        style = VIDEO_STYLE_MAP.get(parts[1] if len(parts) > 1 else "a", "whiteboard")
        tg_send(f"🎬 開始生成影片...\n格式：{fmt} | 風格：{style}\n⏳ 請稍候（約 5~10 分鐘）")
        print(f"🎬 生成影片：{fmt} / {style}")
        ok, out = run_nlm_cli("generate", "video", "--format", fmt, "--style", style, "--wait", timeout=600)
        artifact = "video"

    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中（超過等待時間），請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"video_{ts}.mp4"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", artifact, filepath)
    
    if dl_ok:
        tg_send_file(filepath, caption=f"🎬 影片完成！")
        return f"✅ 影片已生成並下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"

# ==========================================
# 簡報生成
# ==========================================
def handle_generate_slide(params: str) -> str:
    """生成簡報"""
    parts = params.strip().split()
    fmt = SLIDE_FORMAT_MAP.get(parts[0] if len(parts) > 0 else "1", "detailed")
    dl_fmt = SLIDE_DL_MAP.get(parts[1] if len(parts) > 1 else "b", "pptx")

    tg_send(f"📊 開始生成簡報...\n格式：{fmt} | 下載：{dl_fmt.upper()}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "slide-deck", "--format", fmt, "--wait", timeout=600)
    
    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"slide_{ts}.{dl_fmt}"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "slide-deck", filepath, "--format", dl_fmt)
    
    if dl_ok:
        tg_send_file(filepath, caption=f"📊 簡報完成！（{dl_fmt.upper()}）")
        return f"✅ 簡報已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"

# ==========================================
# 資訊圖表生成
# ==========================================
def handle_generate_infographic(params: str) -> str:
    """生成資訊圖表"""
    parts = params.strip().split()
    orient = INFOGRAPHIC_ORIENT_MAP.get(parts[0] if len(parts) > 0 else "1", "portrait")
    detail = INFOGRAPHIC_DETAIL_MAP.get(parts[1] if len(parts) > 1 else "b", "standard")

    tg_send(f"🖼️ 開始生成資訊圖表...\n方向：{orient} | 細節：{detail}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "infographic", "--orientation", orient, "--detail", detail, "--wait", timeout=600)
    
    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"infographic_{ts}.png"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "infographic", filepath)
    
    if dl_ok:
        tg_send_file(filepath, caption="🖼️ 資訊圖表完成！")
        return f"✅ 資訊圖表已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"

# ==========================================
# 心智圖生成
# ==========================================
def handle_generate_mindmap() -> str:
    """生成心智圖"""
    tg_send("🗺️ 開始生成心智圖...\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "mind-map", "--wait", timeout=600)
    
    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"mindmap_{ts}.json"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "mind-map", filepath)
    
    if dl_ok:
        tg_send_file(filepath, caption="🗺️ 心智圖完成！")
        return f"✅ 心智圖已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"

# ==========================================
# 報告生成
# ==========================================
def handle_generate_report(params: str) -> str:
    """生成報告"""
    rtype = REPORT_TYPE_MAP.get(params.strip(), None)
    
    if rtype is None:
        # 自訂提示
        instructions = params.strip()
        tg_send(f"📝 開始生成報告...\n⏳ 請稍候")
        ok, out = run_nlm_cli("generate", "report", instructions, "--wait", timeout=600)
    else:
        tg_send(f"📝 開始生成報告...\n類型：{rtype}\n⏳ 請稍候")
        ok, out = run_nlm_cli("generate", "report", "--format", rtype, "--wait", timeout=600)

    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"report_{ts}.md"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "report", filepath)
    
    if dl_ok:
        tg_send_file(filepath, caption="📝 報告完成！")
        return f"✅ 報告已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"

# ==========================================
# 測驗生成
# ==========================================
def handle_generate_quiz(params: str) -> str:
    """生成測驗"""
    parts = params.strip().split()
    qty = QUIZ_QTY_MAP.get(parts[0] if len(parts) > 0 else "2", "standard")
    diff = QUIZ_DIFF_MAP.get(parts[1] if len(parts) > 1 else "b", "medium")
    fmt = QUIZ_FMT_MAP.get(parts[2] if len(parts) > 2 else "i", "json")

    tg_send(f"❓ 開始生成測驗...\n數量：{qty} | 難度：{diff}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "quiz", "--quantity", qty, "--difficulty", diff, "--wait", timeout=600)
    
    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"quiz_{ts}.{fmt}"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "quiz", filepath, "--format", fmt)
    
    if dl_ok:
        tg_send_file(filepath, caption=f"❓ 測驗完成！（{fmt}）")
        return f"✅ 測驗已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"

# ==========================================
# 學習卡生成
# ==========================================
def handle_generate_flashcard(params: str) -> str:
    """生成學習卡"""
    parts = params.strip().split()
    qty = QUIZ_QTY_MAP.get(parts[0] if len(parts) > 0 else "2", "standard")
    diff = QUIZ_DIFF_MAP.get(parts[1] if len(parts) > 1 else "b", "medium")
    fmt = QUIZ_FMT_MAP.get(parts[2] if len(parts) > 2 else "i", "json")

    tg_send(f"🃏 開始生成學習卡...\n數量：{qty} | 難度：{diff}\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "flashcards", "--quantity", qty, "--difficulty", diff, "--wait", timeout=600)
    
    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"flashcard_{ts}.{fmt}"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "flashcards", filepath, "--format", fmt)
    
    if dl_ok:
        tg_send_file(filepath, caption=f"🃏 學習卡完成！（{fmt}）")
        return f"✅ 學習卡已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"


# ==========================================
# 資料表生成
# ==========================================
def handle_generate_datatable(params: str) -> str:
    """生成資料表"""
    prompt = params.strip() or "compare key concepts"
    
    tg_send(f"📈 開始生成資料表...\n⏳ 請稍候")
    ok, out = run_nlm_cli("generate", "data-table", prompt, "--wait", timeout=600)
    
    if not ok:
        if out == "TIMEOUT":
            msg = "⏳ 生成中，請稍後用選項 19 下載"
            tg_send(msg)
            return msg
        return out

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"datatable_{ts}.csv"
    filepath = os.path.join(OUTPUT_DIR, fname)
    dl_ok, out_dl = run_nlm_cli("download", "data-table", filepath)
    
    if dl_ok:
        tg_send_file(filepath, caption="📈 資料表完成！")
        return f"✅ 資料表已下載：{filepath}"
    return f"✅ 生成完成，但下載失敗：{filepath}"