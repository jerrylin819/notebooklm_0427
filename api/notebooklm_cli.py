# 呼叫 notebooklm CLI 的包裝器

import subprocess
import os

def run_nlm_cli(*args, timeout=360) -> tuple[bool, str]:
    """
    執行 notebooklm CLI 指令
    回傳 (成功, 輸出文字)
    """
    cmd = ["notebooklm"] + list(args)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=False,
            timeout=timeout,
            env=env
        )
        stdout_raw = result.stdout or b""
        stderr_raw = result.stderr or b""

        # 優先 UTF-8，fallback cp950
        try:
            output = stdout_raw.decode("utf-8").strip()
        except UnicodeDecodeError:
            output = stdout_raw.decode("cp950", errors="replace").strip()
        
        try:
            err_text = stderr_raw.decode("utf-8").strip()
        except UnicodeDecodeError:
            err_text = stderr_raw.decode("cp950", errors="replace").strip()

        # 檢查認證錯誤
        if "Authentication expired" in output or "Authentication expired" in err_text:
            return False, "AUTH_EXPIRED"
        
        if result.returncode != 0 and err_text:
            return False, err_text
        
        return True, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, repr(e)


def check_auth() -> bool:
    """檢查認證是否有效"""
    ok , out = run_nlm_cli("auth" , "check")
    return ok and "valid" in out.lower()




