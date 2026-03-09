#!/usr/bin/env python3
"""
通用消息推送工具
支持：飞书、Telegram、Webhook
"""

import os
import sys
import json
import requests
from pathlib import Path

def notify_feishu(message: str, account: str = "xuxu") -> bool:
    """通过 OpenClaw 已配置的飞书发送消息"""
    # OpenClaw 会自动处理飞书消息，直接输出即可
    print(f"[飞书:{account}] {message}")
    return True

def notify_telegram(message: str) -> bool:
    """通过 Telegram Bot 发送消息"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("错误：未设置 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    resp = requests.post(url, json=data, timeout=10)
    return resp.status_code == 200

def notify_webhook(message: str, url: str = None) -> bool:
    """通过 Webhook 发送消息（企业微信、钉钉等）"""
    webhook_url = url or os.getenv("WEBHOOK_URL")
    
    if not webhook_url:
        print("错误：未设置 WEBHOOK_URL")
        return False
    
    # 企业微信格式
    data = {
        "msgtype": "text",
        "text": {"content": message}
    }
    
    resp = requests.post(webhook_url, json=data, timeout=10)
    return resp.status_code == 200

def main():
    if len(sys.argv) < 3:
        print("用法: notify.py <channel> <message>")
        print("channel: feishu | telegram | webhook")
        print("示例: notify.py feishu '交易信号：买入 XXX'")
        sys.exit(1)
    
    channel = sys.argv[1]
    message = sys.argv[2]
    
    if channel == "feishu":
        success = notify_feishu(message)
    elif channel == "telegram":
        success = notify_telegram(message)
    elif channel == "webhook":
        success = notify_webhook(message)
    else:
        print(f"错误：未知 channel '{channel}'")
        success = False
    
    print("✓ 发送成功" if success else "✗ 发送失败")

if __name__ == "__main__":
    main()
