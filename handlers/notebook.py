# 筆記本管理（建立、切換、刪除）

import json
from api.notebooklm_cli import run_nlm_cli
from state import save_state , load_state

def create_notebook(title: str) -> tuple[bool , str]:
    """建立新筆記本"""

    ok , out = run_nlm_cli("create" , title)
    if not ok:
        return False, f"❌ 建立失敗：{out}"
    
    if "Created notebook:" in out:
        #NotebookLM 會回： Created notebook: 1234-xxxx - 我的筆記
        # 解析 notebook ID
        # 輸出格式：Created notebook: <id> - <title>
        parts = out.split("Created notebook:")[-1].strip().split(" - ")
        nb_id = parts[0].strip()
        state = load_state()
        state["notebook_id"] = nb_id
        state["notebook_title"] = title
        save_state(state)
        # 同步 use
        run_nlm_cli("use" ,nb_id)

    return True , out


def list_notebooks() -> str:
    """列出所有筆記本"""
    ok , out = run_nlm_cli("list" , "--json")
    #等於notebooklm list --json
    if ok :
        try:
            import json as _json
            data = _json.loads(out)
            notebooks = data.get("notebooks" , data) if isinstance(data , dict) else data
            if not notebooks:
                return "📒 目前沒有任何筆記本，請先建立一個！" \
        
            lines = ["筆記本列表：\n"]
            for i , nb in enumerate(notebooks , 1):
                nb_id = nb.get("id" , "")
                title = nb.get("title" , "(無標題)")
                created = nb.get("created_at" , nb.get("created", ""))[:10]
                lines.append(f"{i}. {title}")
                lines.append(f"   📅 {created}")
                lines.append(f"   🔑 {nb_id}\n")

                """
                變成這樣：

                1. 我的筆記
                    📅 2026-04-27
                    🔑 xxxx-xxxx
                """
            
            return "\n".join(lines)
        except Exception:
            pass
    
    return out if ok else f"❌ 無法取得筆記本列表：{out}"

def use_notebook(nb_id_or_title: str) -> tuple[bool , str]:
    """切換筆記本"""
    target_id = nb_id_or_title
    target_title = nb_id_or_title[:8] + "..."

    # 如果不像 UUID，嘗試用名稱查 ID，uuid 通常是 xxxx-xxxx 這種格式，如果沒有 - 就當作標題來找
    if "-" not in nb_id_or_title:
        ok_1 , out_1 = run_nlm_cli("list" , "--json")
        if ok_1:
            try:
                data = json.loads(out_1)
                notebooks = data.get("notebooks" , data) if isinstance(data , dict) else data
                for nb in notebooks:
                    if nb.get("title" , "") ==nb_id_or_title:
                        target_id = nb["id"]
                        target_title = nb["title"]
                        break
                else:
                    return False , f"❌ 找不到標題為「{nb_id_or_title}」的筆記本"
            except Exception:
                pass
    
    ok , out  = run_nlm_cli("use" , target_id)
    if not ok:
        return False , f"❌ 切換失敗：{out}"
    
    state = load_state()
    state["notebook_id"] = target_id
    state["notebook_title"] = target_title
    save_state(state)

    return True , out