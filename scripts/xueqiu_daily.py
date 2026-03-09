#!/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3
"""
雪球日报定时任务
每天早上8点抓取并发送到飞书 + 归档到 Obsidian
使用 Playwright 版本（更稳定）
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from xueqiu_playwright import XueQiuPlaywrightTracker

def send_to_feishu(message: str):
    """通过 OpenClaw 发送消息到飞书"""
    # OpenClaw 会自动处理输出，直接打印即可
    print(message)
    return True

async def main():
    """定时任务入口"""
    print(f"⏰ [{datetime.now()}] 开始执行雪球日报任务")
    
    tracker = XueQiuPlaywrightTracker()
    feishu_msg, obsidian_content, success = await tracker.run(save_to_obsidian=True)
    
    if success:
        # 发送到飞书
        send_to_feishu(feishu_msg)
        print("✅ 任务完成")
    else:
        print("❌ 任务失败")

if __name__ == "__main__":
    asyncio.run(main())
