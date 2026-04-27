"""
🦞 NotebookLM 小龍蝦助手
一個功能完整的 NotebookLM 互動助手
"""

__version__ = "1.0.0"
__author__ = "Jerry Lin"
__description__ = "NotebookLM 互動助手（終端機 + Telegram Bot）"

from config import validate_config
from main import main

__all__ = [
    'main',
    'validate_config',
]