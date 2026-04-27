"""業務邏輯處理模組"""

from .notebook import create_notebook, list_notebooks, use_notebook
from .source import add_source, list_sources, research_and_add
from .qa import ask_question
from .generate import (
    handle_generate_audio,
    handle_generate_video,
    handle_generate_slide,
    handle_generate_infographic,
    handle_generate_mindmap,
    handle_generate_report,
    handle_generate_quiz,
    handle_generate_flashcard,
    handle_generate_datatable,
)
from .auth import re_auth, check_auth_status
from .download import download_artifact

__all__ = [
    # notebook
    'create_notebook',
    'list_notebooks',
    'use_notebook',
    
    # source
    'add_source',
    'list_sources',
    'research_and_add',
    
    # qa
    'ask_question',
    
    # generate
    'handle_generate_audio',
    'handle_generate_video',
    'handle_generate_slide',
    'handle_generate_infographic',
    'handle_generate_mindmap',
    'handle_generate_report',
    'handle_generate_quiz',
    'handle_generate_flashcard',
    'handle_generate_datatable',
    
    # auth
    're_auth',
    'check_auth_status',
    
    # download
    'download_artifact',
]