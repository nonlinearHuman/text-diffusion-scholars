#!/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3
"""
雪球用户动态 - RSSHub 方案（无需Cookie）
更安全、更稳定、更简单
"""

import feedparser
from datetime import datetime, timedelta
from pathlib import Path
import json
import time
from typing import List, Dict, Tuple

# 配置
CONFIG = {
    "user_id": "1247297532",  # 大道无形我有型的用户ID
    "username": "大道无形我有型",
    "rsshub_url": "http://localhost:1200/xueqiu/user/{user_id}",
    "data_file": Path(__file__).parent / "xueqiu_rsshub_data.json",
    "obsidian_vault": Path.home() / "Documents" / "obsidian" / "Xun",
}


class XueQiuRSSTracker:
    """基于 RSSHub 的雪球追踪器 - 无需Cookie"""

    def __init__(self):
        self.rss_url = CONFIG["rsshub_url"].format(user_id=CONFIG["user_id"])

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

    def fetch_rss(self) -> Tuple[List[Dict], str]:
        """获取 RSS feed"""
        print(f"📡 正在获取 RSS: {self.rss_url}")

        try:
            feed = feedparser.parse(self.rss_url)

            if feed.bozo:  # RSS 解析错误
                error_msg = f"RSS 解析错误: {feed.bozo_exception}"
                print(f"❌ {error_msg}")
                print(f"Feed status: {feed.get('status', 'unknown')}")
                print(f"Feed entries: {len(feed.entries)}")
                return [], error_msg

            posts = []
            for entry in feed.entries:
                # 解析时间
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                if published:
                    pub_time = datetime(*published[:6])
                else:
                    pub_time = datetime.now()

                posts.append({
                    "id": entry.get("id", entry.get("link", "")),
                    "title": entry.get("title", ""),
                    "text": entry.get("summary", entry.get("description", "")),
                    "created_at": int(pub_time.timestamp() * 1000),
                    "created_at_str": pub_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "url": entry.get("link", ""),
                })

            return posts, ""

        except Exception as e:
            return [], f"获取RSS失败: {e}"

    def filter_yesterday_posts(self, posts: List[Dict]) -> List[Dict]:
        """筛选昨天的发言"""
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")

        filtered = []
        for post in posts:
            post_date = datetime.fromtimestamp(post["created_at"] / 1000).strftime("%Y-%m-%d")
            if post_date == yesterday_str:
                filtered.append(post)

        return filtered

    def format_message(self, posts: List[Dict], for_obsidian: bool = False) -> str:
        """格式化消息"""
        if not posts:
            return f"📭 昨天 {CONFIG['username']} 没有新发言"

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        if for_obsidian:
            # Obsidian 格式
            content = f"# {CONFIG['username']} 发言记录\n\n"
            content += f"**日期**：{yesterday}\n"
            content += f"**数量**：{len(posts)} 条\n"
            content += f"**用户**：[{CONFIG['username']}](https://xueqiu.com/u/{CONFIG['user_id']})\n"
            content += f"**数据源**：[RSSHub]({self.rss_url})\n\n"
            content += "---\n\n"

            for i, post in enumerate(posts, 1):
                content += f"## {i}. {post['created_at_str']}\n\n"
                if post['title']:
                    content += f"**{post['title']}**\n\n"
                content += f"{post['text']}\n\n"
                content += f"[查看原文]({post['url']})\n\n"
                content += "---\n\n"
        else:
            # 飞书推送格式
            content = f"📊 {CONFIG['username']} 昨日发言汇总 ({yesterday})\n"
            content += f"共 {len(posts)} 条\n\n"

            for i, post in enumerate(posts, 1):
                text = post["text"][:200]
                if len(post["text"]) > 200:
                    text += "..."

                content += f"{i}. [{post['created_at_str']}]\n"
                content += f"{text}\n"
                content += f"🔗 {post['url']}\n\n"

        return content

    def save_to_obsidian(self, posts: List[Dict], content: str) -> bool:
        """保存到 Obsidian"""
        if not posts:
            print("📭 没有发言，跳过归档")
            return False

        archives_dir = CONFIG["obsidian_vault"] / "archives"
        archives_dir.mkdir(parents=True, exist_ok=True)

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        filename = f"雪球-{CONFIG['username']}-{yesterday}.md"
        filepath = archives_dir / filename

        # YAML 元数据
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

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(frontmatter + content)
            print(f"✅ 已归档到 Obsidian: {filepath}")
            return True
        except Exception as e:
            print(f"❌ 归档失败: {e}")
            return False

    def run(self, save_to_obsidian: bool = True) -> Tuple[str, str, bool]:
        """主流程"""
        print(f"🔍 开始抓取 {CONFIG['username']} 的动态（RSSHub）...")

        # 获取 RSS
        posts, error = self.fetch_rss()
        if error:
            return f"❌ {error}", "", False

        if not posts:
            return "❌ 获取数据失败，RSS feed 为空", "", False

        print(f"✅ 获取到 {len(posts)} 条动态")

        # 筛选昨天的发言
        yesterday_posts = self.filter_yesterday_posts(posts)

        # 加载历史数据，过滤已推送的
        data = self.load_data()
        existing_ids = {p["id"] for p in data["posts"]}
        new_posts = [p for p in yesterday_posts if p["id"] not in existing_ids]

        # 更新数据
        data["posts"].extend(new_posts)
        data["posts"] = data["posts"][-100:]
        data["last_check"] = datetime.now().isoformat()
        self.save_data(data)

        # 格式化消息
        feishu_msg = self.format_message(new_posts if new_posts else yesterday_posts, for_obsidian=False)
        obsidian_content = self.format_message(yesterday_posts, for_obsidian=True)

        # 保存到 Obsidian
        if save_to_obsidian:
            self.save_to_obsidian(yesterday_posts, obsidian_content)

        print(f"✅ 抓取完成，昨天共 {len(yesterday_posts)} 条发言")

        return feishu_msg, obsidian_content, True


def main():
    """主函数"""
    print(f"⏰ [{datetime.now()}] 开始执行雪球日报任务（RSSHub）")

    tracker = XueQiuRSSTracker()
    feishu_msg, obsidian_content, success = tracker.run(save_to_obsidian=True)

    if success:
        print("\n" + feishu_msg)
        print("\n✅ 任务完成")
    else:
        print("❌ 任务失败")


if __name__ == "__main__":
    main()
