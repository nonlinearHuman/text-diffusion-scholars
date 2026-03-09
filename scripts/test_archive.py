#!/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3
"""
测试雪球归档功能（模拟数据）
"""

from datetime import datetime, timedelta
from pathlib import Path

# 模拟数据
MOCK_POSTS = [
    {
        "id": 1234567890,
        "text": "今天苹果跌了一点，我觉得是加仓的好机会。长期来看，苹果的商业模式依然非常优秀，现金流充沛，管理层也很靠谱。",
        "created_at": int((datetime.now() - timedelta(days=1, hours=10)).timestamp() * 1000),
        "reply_count": 234,
        "retweet_count": 56,
        "like_count": 1892,
    },
    {
        "id": 1234567891,
        "text": "有人问我茅台怎么看？我觉得茅台是个好公司，但估值确实不便宜。投资要讲究安全边际，好公司也要好价格。",
        "created_at": int((datetime.now() - timedelta(days=1, hours=8)).timestamp() * 1000),
        "reply_count": 456,
        "retweet_count": 123,
        "like_count": 3456,
    },
    {
        "id": 1234567892,
        "text": "价值投资的核心是买股票就是买公司。不要盯着股价的波动，而要关注企业的内在价值。时间是好公司的朋友。",
        "created_at": int((datetime.now() - timedelta(days=1, hours=2)).timestamp() * 1000),
        "reply_count": 789,
        "retweet_count": 234,
        "like_count": 5678,
    },
]

def format_obsidian(posts):
    """格式化为 Obsidian markdown"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    content = f"# 大道无形我有型 发言记录\n\n"
    content += f"**日期**：{yesterday}\n"
    content += f"**数量**：{len(posts)} 条\n"
    content += f"**用户**：[大道无形我有型](https://xueqiu.com/u/1247297532)\n\n"
    content += "---\n\n"
    
    for i, post in enumerate(posts, 1):
        created_at_str = datetime.fromtimestamp(post["created_at"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        content += f"## {i}. {created_at_str}\n\n"
        content += f"{post['text']}\n\n"
        content += f"**互动数据**：💬 {post['reply_count']} | 🔄 {post['retweet_count']} | ❤️ {post['like_count']}\n\n"
        content += f"[查看原文](https://xueqiu.com/{post['id']})\n\n"
        content += "---\n\n"
    
    return content, yesterday

def test_archive():
    """测试归档功能"""
    print("🧪 测试雪球归档功能...")
    
    # 生成内容
    content, yesterday = format_obsidian(MOCK_POSTS)
    
    # Obsidian vault 路径
    vault_path = Path.home() / "Documents" / "obsidian" / "Xun"
    archives_dir = vault_path / "archives"
    
    # 创建目录
    archives_dir.mkdir(parents=True, exist_ok=True)
    
    # 文件名
    filename = f"雪球-大道无形我有型-{yesterday}.md"
    filepath = archives_dir / filename
    
    # 添加元数据
    frontmatter = f"""---
title: 大道无形我有型 发言记录
date: {yesterday}
source: 雪球
user: 大道无形我有型
user_id: 1247297532
count: {len(MOCK_POSTS)}
tags:
  - 雪球
  - 投资
  - 大道无形我有型
---

"""
    
    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)
    
    print(f"✅ 测试完成！")
    print(f"📄 文件位置: {filepath}")
    print(f"\n内容预览：\n{content[:500]}...")

if __name__ == "__main__":
    test_archive()
