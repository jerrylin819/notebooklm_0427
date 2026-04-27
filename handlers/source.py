# 來源管理（新增、列表）
from api.notebooklm_cli import run_nlm_cli
from state import load_state
from integrations.telegram import tg_send

def add_source(source: str) -> tuple[bool, str]:
    """新增來源"""
    state = load_state()
    if not state.get("notebook_id"):
        return False, "❌ 尚未選擇筆記本，請先切換或建立筆記本"
    
    ok, out = run_nlm_cli("source", "add", source)
    if not ok:
        return False, f"❌ 新增來源失敗：{out}"
    
    tg_send(f"✅ 來源已新增：{source}")
    return True, out

def list_sources() -> str:
    """列出所有來源"""
    ok, out = run_nlm_cli("source", "list")
    if not ok:
        return f"❌ 列出來源失敗：{out}"
    return out if out else "（目前沒有來源）"

def research_and_add(topic: str) -> str:
    """網路研究並自動匯入"""
    state = load_state()
    if not state.get("notebook_id"):
        return "❌ 尚未選擇筆記本"
    
    tg_send(f"🔍 開始網路研究：{topic}\n⏳ 請稍候...")
    ok, out = run_nlm_cli("source", "add-research", topic, timeout=180)
    
    if ok:
        tg_send(f"✅ 研究完成，來源已匯入")
        return f"✅ 研究完成，來源已匯入\n{out}"
    else:
        return f"❌ 研究失敗：{out}"