"""Crop advisory prompts"""

from .openai import OPENAI_PROMPTS
from .claude import CLAUDE_PROMPTS
from .llama import LLAMA_PROMPTS

__all__ = ["OPENAI_PROMPTS", "CLAUDE_PROMPTS", "LLAMA_PROMPTS"]