# 自然語言解析（GPT-4o）

import json
from config import OPENAI_API_KEY

def parse_natural_language(user_input: str) -> dict:
    """用 GPT-4o 解析自然語言指令"""
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    system = """你是 NotebookLM 小龍蝦助手的意圖解析器。
根據使用者輸入，回傳 JSON，格式如下：
{
  "action": "menu | create | list | use | add_source | ask | audio | ...",
  "params": "相關參數（字串）",
  "confirm_needed": true/false,
  "confirm_msg": "需要確認時的提示訊息"
}
規則：
- 不確定的操作（刪除、切換筆記本）confirm_needed = true
- 明確的生成/下載指令 confirm_needed = false
- 無法理解的輸入 action = unknown
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"},
            max_tokens=300,
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)

    except Exception as e :
        return {"action": "unknown", "params": "", "confirm_needed": False, 
                "confirm_msg": ""}