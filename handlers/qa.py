# 問答功能
from api.notebooklm_cli import run_nlm_cli
from state import load_state
from integrations.telegram import tg_send

# ==========================================
# 問答功能
# ==========================================

def ask_question(question: str) -> tuple[bool, str]:
    """向筆記本提問"""
    state = load_state()
    if not state.get("notebook_id"):
        return False, "❌ 尚未選擇筆記本"
    
    tg_send(f"💬 正在處理你的問題...\n⏳ 請稍候")
    ok, out = run_nlm_cli("ask", question, timeout=120)
    
    if not ok:
        return False, f"❌ 問答失敗：{out}"
    
    # 摘要並推播結果
    if len(out) > 1000:
        summary = out[:1000] + "..."
        tg_send(f"💬 問答結果（摘錄）：\n{summary}")
    else:
        tg_send(f"💬 問答結果：\n{out}")
    
    return True, out