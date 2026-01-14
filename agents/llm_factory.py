"""
Factory module to create and configure LLM chat instances using OpenRouter.
"""

import os

from autogen_ext.models._openai._openai_client import OpenAIChatCompletionClient
from langchain_openai import ChatOpenAI

from agents.config import OPENROUTER_BASE_URL, OPENROUTER_MODEL, USE_OPENROUTER

def _get_openrouter_headers():
    """Optional headers for OpenRouter routing/attribution."""
    return {
        # "HTTP-Referer": "https://your-site-or-localhost",  # optional
        # "X-Title": "GLOSS",  # optional
    }

def _require_openrouter_key():
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    return key


def get_llmchat():
    """Return a configured chat LLM instance (OpenRouter only)."""
    if not USE_OPENROUTER:
        raise ValueError("OpenRouter must be enabled; Azure/OpenAI direct paths removed")
    

    return ChatOpenAI(
        openai_api_key=_require_openrouter_key(),
        model_name=OPENROUTER_MODEL,
        base_url=OPENROUTER_BASE_URL,
        temperature=0,
        default_headers=_get_openrouter_headers(),
    )


def get_llm_chat_openai(model_name: str = OPENROUTER_MODEL, temperature: float = 0):
    """Return a configured OpenRouter chat client for autogen_ext."""
    key = _require_openrouter_key()
    return OpenAIChatCompletionClient(
        openai_api_key=key,
        model=model_name,
        temperature=temperature,
        base_url=OPENROUTER_BASE_URL,
        extra_headers=_get_openrouter_headers(),
    )
