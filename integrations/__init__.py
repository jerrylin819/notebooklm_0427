"""外部服務集成模組"""

from .telegram import tg_send, tg_send_file, TelegramBot

__all__ = [
    'tg_send',
    'tg_send_file',
    'TelegramBot',
]