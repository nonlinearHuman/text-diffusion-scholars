#!/usr/bin/env python3
"""
雪球用户动态追踪器
每天抓取"大道无形我有型"（段永平）的发言并推送
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# 配置
CONFIG = {
    "user_id": "1247297532",  # 大道无形我有型的用户ID
    "username": "大道无形我有型",
    "api_url": "https://xueqiu.com/v4/statuses/user_timeline.json",
    "data_file": Path(__file__).parent / "xueqiu_data.json",
    "cookie": os.getenv("XUEQIU_COOKIE", ""),
}

class XueQiuTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": f"https://xueqiu.com/u/{CONFIG['user_id']}",
        })
        
        # 设置cookie（如果有的话）
        if CONFIG["cookie"]:
            self.session.headers["Cookie"] = CONFIG["cookie"]
    
    def load_data(self) -> Dict:
        """加载历史数据"""
        if CONFIG["data_file"].exists():
            with open(CONFIG["data_file"], "r", encoding="utf-8") as f:
                return json.load(f)
        return {"posts": [], "last_check": None}
    
    def save_data(self, data: Dict):
        """保存数据"""
        with open(CONFIG["data_file"], "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def fetch_posts(self, page: int = 1, count: int = 20) -> Optional[List[Dict]]:
        """获取用户动态"""
        params = {
            "user_id": CONFIG["user_id"],
            "page": page,
            "count": count,
        }
        
        try:
            resp = self.session.get(CONFIG["api_url"], params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("statuses", [])
        except Exception as e:
            print(f"❌ 获取数据失败: {e}")
            return None
    
    def filter_yesterday_posts(self, posts: List[Dict]) -> List[Dict]:
        """筛选昨天的发言"""
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        
        filtered = []
        for post in posts:
            # 解析时间
            created_at = post.get("created_at", 0)
            post_date = datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d")
            
            if post_date == yesterday_str:
                filtered.append({
                    "id": post["id"],
                    "text": post.get("text", ""),
                    "created_at": created_at,
                    "created_at_str": datetime.fromtimestamp(created_at / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                    "retweet_count": post.get("retweet_count", 0),
                    "reply_count": post.get("reply_count", 0),
                    "like_count": post.get("like_count", 0),
                    "url": f"https://xueqiu.com/{post['id']}",
                })
        
        return filtered
    
    def format_message(self, posts: List[Dict], for_obsidian: bool = False) -> str:
        """格式化消息
        
        Args:
            posts: 发言列表
            for_obsidian: 是否为 Obsidian 格式（True 时保留完整内容）
        """
        if not posts:
            return f"📭 昨天 {CONFIG['username']} 没有新发言"
        
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        if for_obsidian:
            # Obsidian 格式 - 保留完整内容
            msg = f"# {CONFIG['username']} 发言记录\n\n"
            msg += f"**日期**：{yesterday}\n"
            msg += f"**数量**：{len(posts)} 条\n"
            msg += f"**用户**：[{CONFIG['username']}](https://xueqiu.com/u/{CONFIG['user_id']})\n\n"
            msg += "---\n\n"
            
            for i, post in enumerate(posts, 1):
                msg += f"## {i}. {post['created_at_str']}\n\n"
                msg += f"{post['text']}\n\n"
                msg += f"**互动数据**：💬 {post['reply_count']} | 🔄 {post['retweet_count']} | ❤️ {post['like_count']}\n\n"
                msg += f"[查看原文]({post['url']})\n\n"
                msg += "---\n\n"
        else:
            # 飞书推送格式 - 限制长度
            msg = f"📊 {CONFIG['username']} 昨日发言汇总 ({yesterday})\n"
            msg += f"共 {len(posts)} 条\n\n"
            
            for i, post in enumerate(posts, 1):
                text = post["text"][:200]  # 限制长度
                if len(post["text"]) > 200:
                    text += "..."
                
                msg += f"{i}. [{post['created_at_str']}]\n"
                msg += f"{text}\n"
                msg += f"💬 {post['reply_count']} 🔄 {post['retweet_count']} ❤️ {post['like_count']}\n"
                msg += f"🔗 {post['url']}\n\n"
        
        return msg
    
    def save_to_obsidian(self, posts: List[Dict], content: str) -> bool:
        """保存到 Obsidian
        
        Args:
            posts: 发言列表
            content: markdown 内容
            
        Returns:
            是否成功
        """
        if not posts:
            print("📭 没有发言，跳过归档")
            return False
        
        # Obsidian vault 路径
        vault_path = Path.home() / "Documents" / "obsidian" / "Xun"
        archives_dir = vault_path / "archives"
        
        # 创建 archives 目录
        archives_dir.mkdir(parents=True, exist_ok=True)
        
        # 文件名：雪球-大道无形我有型-2026-03-05.md
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        filename = f"雪球-{CONFIG['username']}-{yesterday}.md"
        filepath = archives_dir / filename
        
        # 添加元数据
        frontmatter = f"""---
title: {CONFIG['username']} 发言记录
date: {yesterday}
source: 雪球
user: {CONFIG['username']}
user_id: {CONFIG['user_id']}
count: {len(posts)}
tags:
  - 雪球
  - 投资
  - {CONFIG['username']}
---

"""
        
        # 写入文件
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(frontmatter + content)
            print(f"✅ 已归档到 Obsidian: {filepath}")
            return True
        except Exception as e:
            print(f"❌ 归档失败: {e}")
            return False
    
    def run(self, save_to_obsidian: bool = True) -> tuple:
        """主流程
        
        Args:
            save_to_obsidian: 是否保存到 Obsidian
            
        Returns:
            (飞书消息, Obsidian内容, 是否成功)
        """
        print(f"🔍 开始抓取 {CONFIG['username']} 的动态...")
        
        # 加载历史数据
        data = self.load_data()
        existing_ids = {p["id"] for p in data["posts"]}
        
        # 获取最新动态
        posts = self.fetch_posts(page=1, count=50)
        if not posts:
            return "❌ 获取数据失败，请检查网络或Cookie", "", False
        
        # 筛选昨天的发言
        yesterday_posts = self.filter_yesterday_posts(posts)
        
        # 过滤已推送的
        new_posts = [p for p in yesterday_posts if p["id"] not in existing_ids]
        
        # 更新数据
        data["posts"].extend(new_posts)
        data["posts"] = data["posts"][-100:]  # 只保留最近100条
        data["last_check"] = datetime.now().isoformat()
        self.save_data(data)
        
        # 格式化消息（飞书）
        feishu_msg = self.format_message(new_posts if new_posts else yesterday_posts, for_obsidian=False)
        
        # 格式化消息（Obsidian）
        obsidian_content = self.format_message(yesterday_posts, for_obsidian=True)
        
        # 保存到 Obsidian
        if save_to_obsidian:
            self.save_to_obsidian(yesterday_posts, obsidian_content)
        
        print(f"✅ 抓取完成，找到 {len(yesterday_posts)} 条发言")
        
        return feishu_msg, obsidian_content, True


def main():
    """主函数"""
    tracker = XueQiuTracker()
    message = tracker.run()
    print(message)
    
    # 返回消息供外部调用
    return message


if __name__ == "__main__":
    main()
