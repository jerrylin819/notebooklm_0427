# 工具函數（檔案操作、時間戳等
"""工具函數集"""

import os
from datetime import datetime
from pathlib import Path

# ==========================================
# 時間工具
# ==========================================

def get_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """
    取得格式化的時間戳
    
    參數：
        format_str: 時間格式字符串
    
    回傳：
        格式化的時間戳字符串
    """
    return datetime.now().strftime(format_str)

# ==========================================
# 檔案工具
# ==========================================

def ensure_dir(path: str) -> bool:
    """
    確保目錄存在，不存在則建立
    
    參數：
        path: 目錄路徑
    
    回傳：
        是否成功
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"❌ 建立目錄失敗：{path}\n{e}")
        return False

def safe_filename(filename: str) -> str:
    """
    將檔名進行安全化處理（移除非法字符）
    
    參數：
        filename: 原始檔名
    
    回傳：
        安全化後的檔名
    """
    # 移除非法字符
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    safe_name = filename
    for char in illegal_chars:
        safe_name = safe_name.replace(char, '_')
    return safe_name

def file_exists(filepath: str) -> bool:
    """檢查檔案是否存在"""
    return Path(filepath).exists()

def get_file_size(filepath: str) -> int:
    """取得檔案大小（字節）"""
    try:
        return Path(filepath).stat().st_size
    except Exception:
        return 0

def format_file_size(size_bytes: int) -> str:
    """
    將檔案大小格式化為可讀的字符串
    
    參數：
        size_bytes: 檔案大小（字節）
    
    回傳：
        格式化後的大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

# ==========================================
# 驗證工具
# ==========================================

def is_valid_url(url: str) -> bool:
    """檢查是否為有效的 URL"""
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def is_valid_youtube_url(url: str) -> bool:
    """檢查是否為有效的 YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
    return any(domain in url for domain in youtube_domains) if is_valid_url(url) else False

# ==========================================
# 文字工具
# ==========================================

def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    截斷文字到指定長度
    
    參數：
        text: 原始文字
        max_length: 最大長度
        suffix: 截斷後的後綴
    
    回傳：
        截斷後的文字
    """
    if len(text) > max_length:
        return text[:max_length - len(suffix)] + suffix
    return text

def format_list(items: list, separator: str = "\n") -> str:
    """
    將列表格式化為字符串
    
    參數：
        items: 項目列表
        separator: 分隔符
    
    回傳：
        格式化後的字符串
    """
    return separator.join(f"• {item}" for item in items)