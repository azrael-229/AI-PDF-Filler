"""
AI Provider Abstraction Layer

This module provides a unified interface for multiple AI providers that support
the OpenAI API format. This includes:
- Ollama (local)
- LM Studio (local)
- vLLM (local/cloud)
- OpenAI (cloud)
- Any other OpenAI-compatible endpoint

Usage:
    from ai_provider import get_ai_response
    
    # Using default configuration (Ollama)
    response = get_ai_response(prompt, context)
    
    # Using custom provider
    response = get_ai_response(
        prompt, 
        context, 
        api_key="your-api-key",
        base_url="http://localhost:1234/v1",  # LM Studio default
        model="your-model-name"
    )
"""

import json
import requests
from typing import Optional


class AIProviderError(Exception):
    """Custom exception for AI provider errors."""
    pass


def get_ai_response(
    prompt: str, 
    context: str = "",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout: int = 60
) -> str:
    """
    Get AI response from an OpenAI-compatible API provider.
    
    Args:
        prompt: The user's prompt/question
        context: Additional context to prepend to the prompt
        api_key: API key for authenticated providers (e.g., OpenAI). 
                 Set to None or empty string for local providers like Ollama/LM Studio.
        base_url: Base URL of the API endpoint. Defaults to Ollama's default if not specified.
                  Examples:
                    - Ollama: "http://localhost:11434" (uses /api/generate)
                    - LM Studio: "http://localhost:1234/v1" (OpenAI compatible)
                    - OpenAI: "https://api.openai.com/v1"
        model: Model name to use. Defaults to DEFAULT_MODEL if not specified.
        timeout: Request timeout in seconds
        
    Returns:
        The AI's response as a string
        
    Raises:
        AIProviderError: If the API call fails or returns an error
    """
    
    # Use provided values or fall back to defaults
    target_model = model if model and model.strip() else DEFAULT_MODEL
    
    # Determine which provider type we're using based on base_url
    if base_url:
        if "localhost" in base_url or "127.0.0.1" in base_url:
            # Likely a local provider (Ollama, LM Studio, etc.)
            return _call_local_provider(prompt, context, target_model, base_url, api_key, timeout)
        else:
            # Assume cloud provider with OpenAI-compatible API
            return _call_openai_compatible_api(prompt, context, target_model, base_url, api_key, timeout)
    else:
        # Default to Ollama if no URL specified
        return _call_ollama(prompt, context, target_model, timeout)


def _call_ollama(
    prompt: str, 
    context: str, 
    model: str, 
    timeout: int = 60
) -> str:
    """Call Ollama API (legacy method for backward compatibility)."""
    
    url = "http://localhost:11434/api/generate"
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    
    data = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=timeout)
        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            raise AIProviderError(f"Ollama API error: {response.status_code}, {response.text}")
    except Exception as e:
        raise AIProviderError(f"Connection error to Ollama: {str(e)}")


def _call_local_provider(
    prompt: str, 
    context: str, 
    model: str, 
    base_url: str, 
    api_key: Optional[str], 
    timeout: int = 60
) -> str:
    """Call a local OpenAI-compatible provider (LM Studio, vLLM, etc.)."""
    
    # Determine if this is an Ollama-style endpoint or OpenAI-style
    if "/api/generate" in base_url or "11434" in base_url:
        return _call_ollama(prompt, context, model, timeout)
    
    # Use OpenAI-compatible format for other local providers
    url = f"{base_url.rstrip('/')}/chat/completions" if not base_url.endswith("/chat/completions") else base_url
    
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides concise answers."},
            {"role": "user", "content": full_prompt}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise AIProviderError(f"API error: {response.status_code}, {response.text}")
    except Exception as e:
        raise AIProviderError(f"Connection error to {base_url}: {str(e)}")


def _call_openai_compatible_api(
    prompt: str, 
    context: str, 
    model: str, 
    base_url: str, 
    api_key: Optional[str], 
    timeout: int = 60
) -> str:
    """Call a cloud OpenAI-compatible API."""
    
    url = f"{base_url}/chat/completions" if not base_url.endswith("/chat/completions") else base_url
    
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}" if api_key else ""
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides concise answers."},
            {"role": "user", "content": full_prompt}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            raise AIProviderError(f"API error: {response.status_code}, {response.text}")
    except Exception as e:
        raise AIProviderError(f"Connection error to {base_url}: {str(e)}")


# Default configuration
DEFAULT_MODEL = "gemma4:E4b"  # Can be changed to any model supported by your provider
