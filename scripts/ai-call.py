#!/usr/bin/env python3
"""
通用 AI API 调用工具
支持：智谱 GLM、OpenAI、DeepSeek
"""

import os
import sys
import json
import requests
from pathlib import Path

# 加载配置
CONFIG_FILE = Path(__file__).parent / "services.json"
if CONFIG_FILE.exists():
    with open(CONFIG_FILE) as f:
        CONFIG = json.load(f)
else:
    CONFIG = {}

def call_zhipu(prompt: str, model: str = "glm-4-flash") -> str:
    """调用智谱 GLM API"""
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key:
        # 尝试从 openclaw.json 读取
        openclaw_config = Path.home() / ".openclaw" / "openclaw.json"
        if openclaw_config.exists():
            with open(openclaw_config) as f:
                oc = json.load(f)
                # 智谱 API key 可能在这里，需要你手动配置
        
    if not api_key:
        return "错误：未设置 ZHIPU_API_KEY 环境变量"
    
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """调用 OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "错误：未设置 OPENAI_API_KEY 环境变量"
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_deepseek(prompt: str, model: str = "deepseek-chat") -> str:
    """调用 DeepSeek API - 性价比高，适合文案生成"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "错误：未设置 DEEPSEEK_API_KEY 环境变量"
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def main():
    if len(sys.argv) < 3:
        print("用法: ai-call.py <provider> <prompt>")
        print("provider: zhipu | openai | deepseek")
        print("示例: ai-call.py deepseek '写一个小红书文案'")
        sys.exit(1)
    
    provider = sys.argv[1]
    prompt = sys.argv[2]
    
    if provider == "zhipu":
        result = call_zhipu(prompt)
    elif provider == "openai":
        result = call_openai(prompt)
    elif provider == "deepseek":
        result = call_deepseek(prompt)
    else:
        result = f"错误：未知 provider '{provider}'"
    
    print(result)

if __name__ == "__main__":
    main()
