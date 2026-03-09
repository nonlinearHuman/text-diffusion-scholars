#!/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3
"""
雪球用户动态追踪 - Playwright 方案
支持 Cookie 登录，绕过反爬限制
"""

import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json
import os
import re
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

# 配置
CONFIG = {
    "user_id": "1247347556",  # 大道无形我有型的用户ID（修正）
    "username": "大道无形我有型",
    "user_url": "https://xueqiu.com/u/{user_id}",
    "data_file": Path(__file__).parent / "xueqiu_playwright_data.json",
    "obsidian_vault": Path.home() / "Documents" / "obsidian" / "Xun",
    "timeout": 60000,  # 60秒超时
    "headless": True,  # 无头模式，节省资源
    "cookie_env": "XUEQIU_COOKIE",  # Cookie 环境变量名
    "cookie_file": Path(__file__).parent / ".xueqiu_cookie",  # Cookie 文件路径
}


class XueQiuPlaywrightTracker:
    """基于 Playwright 的雪球追踪器"""

    def __init__(self):
        self.user_url = CONFIG["user_url"].format(user_id=CONFIG["user_id"])

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

    def get_cookie(self) -> Optional[str]:
        """获取 Cookie（优先环境变量，其次文件）"""
        # 1. 环境变量
        cookie = os.environ.get(CONFIG["cookie_env"])
        if cookie:
            print(f"✅ 使用环境变量中的 Cookie")
            return cookie
        
        # 2. Cookie 文件
        cookie_file = CONFIG["cookie_file"]
        if cookie_file.exists():
            cookie = cookie_file.read_text().strip()
            if cookie:
                print(f"✅ 使用文件中的 Cookie: {cookie_file}")
                return cookie
        
        return None

    def parse_cookie(self, cookie_str: str) -> List[Dict]:
        """解析 Cookie 字符串为 Playwright 格式"""
        cookies = []
        for item in cookie_str.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": ".xueqiu.com",
                    "path": "/",
                })
        return cookies

    async def fetch_posts(self) -> Tuple[List[Dict], str]:
        """获取用户动态"""
        print(f"🎭 启动浏览器访问：{self.user_url}")

        posts = []
        error_msg = ""
        
        # 获取 Cookie
        cookie_str = self.get_cookie()
        if not cookie_str:
            print(f"⚠️  未配置 Cookie，可能无法访问")
            print(f"💡 配置方式：")
            print(f"   1. 环境变量: export XUEQIU_COOKIE='your_cookie'")
            print(f"   2. 文件: echo 'your_cookie' > {CONFIG['cookie_file']}")

        try:
            async with async_playwright() as p:
                # 启动浏览器（使用 channel='chromium' 或 headless 模式）
                browser = await p.chromium.launch(
                    headless=CONFIG["headless"],
                    channel='chromium',  # 使用已安装的 chromium
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                    ]
                )

                # 创建上下文（模拟真人）
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                )
                
                # 添加 Cookie
                if cookie_str:
                    cookies = self.parse_cookie(cookie_str)
                    await context.add_cookies(cookies)
                    print(f"✅ 已添加 {len(cookies)} 个 Cookie")

                page = await context.new_page()

                try:
                    # 访问用户主页
                    print(f"📡 正在加载页面...")
                    # 使用 domcontentloaded 而不是 networkidle，避免超时
                    await page.goto(self.user_url, timeout=CONFIG["timeout"], wait_until="domcontentloaded")
                    
                    # 额外等待内容加载
                    print(f"⏳ 等待内容加载...")
                    await page.wait_for_timeout(5000)
                    
                    # 截图调试
                    debug_screenshot = "/Users/gesong/.openclaw/workspace/scripts/debug_page.png"
                    await page.screenshot(path=debug_screenshot)
                    print(f"📸 调试截图: {debug_screenshot}")
                    
                    # 检查是否有登录弹窗，尝试点击跳过
                    skip_selectors = [
                        "button:has-text('跳过')",
                        ".login-modal button:has-text('跳过')",
                        "[class*='login'] button:has-text('跳过')",
                    ]
                    
                    for selector in skip_selectors:
                        try:
                            skip_btn = await page.query_selector(selector)
                            if skip_btn:
                                print(f"🔘 检测到登录弹窗，点击跳过...")
                                await skip_btn.click(timeout=5000)
                                await page.wait_for_timeout(3000)
                                break
                        except:
                            continue

                    # 提取发言 - 使用更精确的方法
                    print(f"🔍 正在提取发言...")
                    
                    # 方法：滚动页面加载更多内容，然后提取
                    print(f"📜 滚动页面加载更多内容...")
                    for i in range(3):
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(2000)
                    
                    # 截图调试（滚动后）
                    debug_screenshot2 = "/Users/gesong/.openclaw/workspace/scripts/debug_page_scrolled.png"
                    await page.screenshot(path=debug_screenshot2, full_page=True)
                    print(f"📸 滚动后截图: {debug_screenshot2}")
                    
                    # 使用 JavaScript 提取所有发言内容（改进版 - 更精确的选择器）
                    posts_data = await page.evaluate("""
                        () => {
                            const posts = [];
                            
                            // 查找所有发言卡片
                            // 雪球的发言通常在一个容器中，包含用户信息、时间、内容
                            const cards = document.querySelectorAll('[class*="timeline"], [class*="status"], [class*="item"]');
                            
                            const seen = new Set();
                            
                            for (const card of cards) {
                                try {
                                    // 提取链接
                                    const linkElem = card.querySelector('a[href*="/1247347556/"]');
                                    if (!linkElem) continue;
                                    
                                    const href = linkElem.href;
                                    const match = href.match(/\\/1247347556\\/(\\d+)/);
                                    if (!match) continue;
                                    
                                    const postId = match[1];
                                    if (seen.has(postId)) continue;
                                    seen.add(postId);
                                    
                                    // 提取时间 - 查找包含时间信息的元素
                                    let timeText = '';
                                    const timeElems = card.querySelectorAll('time, span, div');
                                    for (const elem of timeElems) {
                                        const text = elem.textContent.trim();
                                        if (text.includes('昨天') || text.includes('前天') || 
                                            text.match(/\\d+小时前/) || text.match(/\\d+天前/) ||
                                            text.match(/\\d{2}-\\d{2}/)) {
                                            // 提取时间部分（去除其他文字）
                                            const timeMatch = text.match(/(昨天|前天|\\d+小时前|\\d+天前|\\d{2}-\\d{2}[^\\s]*)/);
                                            if (timeMatch) {
                                                timeText = timeMatch[1];
                                                break;
                                            }
                                        }
                                    }
                                    
                                    // 提取内容 - 查找长文本
                                    let content = '';
                                    const contentElems = card.querySelectorAll('div, article');
                                    for (const elem of contentElems) {
                                        const text = elem.textContent.trim();
                                        if (text.length > 30 && !text.includes(timeText)) {
                                            content = text.substring(0, 500);
                                            break;
                                        }
                                    }
                                    
                                    if (content && content.length > 20) {
                                        posts.push({
                                            id: postId,
                                            text: content,
                                            url: href,
                                            time_text: timeText,
                                        });
                                    }
                                    
                                    // 限制数量
                                    if (posts.length >= 30) break;
                                } catch (e) {
                                    // 忽略错误
                                }
                            }
                            
                            return posts;
                        }
                    """)
                    
                    print(f"✅ JavaScript 提取到 {len(posts_data)} 条发言")
                    
                    # 处理提取到的数据
                    for post_data in posts_data[:20]:  # 最多获取20条
                        try:
                            time_text = post_data.get("time_text", "")
                            
                            # 计算时间戳（改进处理）
                            pub_time = datetime.now()
                            time_text_lower = time_text.lower()
                            
                            if "昨天" in time_text:
                                # 昨天 - 提取时间（如果有）
                                pub_time = datetime.now() - timedelta(days=1)
                                # 尝试提取具体时间
                                time_match = re.search(r"(\d{1,2}):(\d{2})", time_text)
                                if time_match:
                                    hour, minute = int(time_match.group(1)), int(time_match.group(2))
                                    pub_time = pub_time.replace(hour=hour, minute=minute)
                            elif "前天" in time_text:
                                pub_time = datetime.now() - timedelta(days=2)
                            elif "小时前" in time_text_lower:
                                hours = time_text_lower.replace("小时前", "").strip()
                                if hours.isdigit():
                                    pub_time = datetime.now() - timedelta(hours=int(hours))
                            elif "分钟前" in time_text_lower:
                                minutes = time_text_lower.replace("分钟前", "").strip()
                                if minutes.isdigit():
                                    pub_time = datetime.now() - timedelta(minutes=int(minutes))
                            elif "天前" in time_text_lower:
                                days = time_text_lower.replace("天前", "").strip()
                                if days.isdigit():
                                    pub_time = datetime.now() - timedelta(days=int(days))
                            elif re.search(r'\d{2}-\d{2}', time_text):
                                # 日期格式 MM-DD
                                date_match = re.search(r'(\d{2})-(\d{2})', time_text)
                                if date_match:
                                    month, day = int(date_match.group(1)), int(date_match.group(2))
                                    year = datetime.now().year
                                    pub_time = datetime(year, month, day)
                            
                            posts.append({
                                "id": post_data.get("id", f"temp_{len(posts)}"),
                                "text": post_data.get("text", ""),
                                "created_at": int(pub_time.timestamp() * 1000),
                                "created_at_str": pub_time.strftime("%Y-%m-%d %H:%M:%S"),
                                "url": post_data.get("url", self.user_url),
                                "time_text": time_text,
                            })
                        
                        except Exception as e:
                            print(f"⚠️  处理单条失败: {e}")
                            continue

                    print(f"✅ 成功处理 {len(posts)} 条发言")

                except PlaywrightTimeoutError:
                    error_msg = "页面加载超时"
                    print(f"❌ {error_msg}")

                finally:
                    # 关闭浏览器
                    await browser.close()

        except Exception as e:
            error_msg = f"浏览器错误: {e}"
            print(f"❌ {error_msg}")

        return posts, error_msg

    def filter_recent_posts(self, posts: List[Dict], days: int = 1) -> List[Dict]:
        """筛选最近N天的发言"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = today - timedelta(days=days)
        
        filtered = []
        for post in posts:
            post_date = datetime.fromtimestamp(post["created_at"] / 1000).replace(hour=0, minute=0, second=0, microsecond=0)
            if post_date >= start_date:
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
            content += f"**用户**：[{CONFIG['username']}]({self.user_url})\n"
            content += f"**数据源**：Playwright 自动化\n\n"
            content += "---\n\n"

            for i, post in enumerate(posts, 1):
                content += f"## {i}. {post['created_at_str']}\n\n"
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

    def save_to_obsidian(self, posts: List[Dict], content: str, days: int = 3) -> bool:
        """保存到 Obsidian
        
        Args:
            posts: 发言列表
            content: markdown 内容
            days: 最近几天
            
        Returns:
            是否成功
        """
        if not posts:
            print("📭 没有发言，跳过归档")
            return False

        archives_dir = CONFIG["obsidian_vault"] / "archives"
        archives_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"雪球-{CONFIG['username']}-最近{days}天-{today}.md"
        filepath = archives_dir / filename

        # YAML 元数据
        frontmatter = f"""---
title: {CONFIG['username']} 发言记录
date: {today}
source: 雪球
user: {CONFIG['username']}
user_id: {CONFIG['user_id']}
count: {len(posts)}
period: 最近{days}天
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

    async def run(self, save_to_obsidian: bool = True) -> Tuple[str, str, bool]:
        """主流程"""
        print(f"🔍 开始抓取 {CONFIG['username']} 的动态（Playwright）...")

        # 获取发言
        posts, error = await self.fetch_posts()
        if error:
            return f"❌ {error}", "", False

        if not posts:
            return "❌ 获取数据失败，未找到发言", "", False

        # 调试：打印所有抓到的发言和时间
        print(f"\n📋 抓取到的所有发言（前10条）：")
        for i, post in enumerate(posts[:10], 1):
            print(f"{i}. [{post['time_text']}] {post['created_at_str']} - {post['text'][:50]}...")
        
        # 筛选最近3天的发言（因为"昨天"的显示会变化）
        recent_posts = self.filter_recent_posts(posts, days=3)
        print(f"\n📊 最近3天的发言：{len(recent_posts)} 条")
        
        # 筛选昨天的发言（用于飞书推送）
        yesterday_posts = self.filter_recent_posts(posts, days=1)
        print(f"📊 昨天的发言：{len(yesterday_posts)} 条")

        # 加载历史数据，过滤已推送的
        data = self.load_data()
        existing_ids = {p["id"] for p in data["posts"]}
        new_posts = [p for p in recent_posts if p["id"] not in existing_ids]

        # 更新数据
        data["posts"].extend(new_posts)
        data["posts"] = data["posts"][-100:]
        data["last_check"] = datetime.now().isoformat()
        self.save_data(data)

        # 格式化消息（飞书推送昨天的）
        feishu_msg = self.format_message(yesterday_posts, for_obsidian=False)
        # Obsidian 归档最近3天的
        obsidian_content = self.format_message(recent_posts, for_obsidian=True)

        # 保存到 Obsidian（最近3天）
        if save_to_obsidian:
            self.save_to_obsidian(recent_posts, obsidian_content, days=3)

        print(f"✅ 抓取完成，最近3天共 {len(recent_posts)} 条发言")

        return feishu_msg, obsidian_content, True


async def main():
    """主函数"""
    print(f"⏰ [{datetime.now()}] 开始执行雪球日报任务（Playwright）")

    tracker = XueQiuPlaywrightTracker()
    feishu_msg, obsidian_content, success = await tracker.run(save_to_obsidian=True)

    if success:
        print("\n" + feishu_msg)
        print("\n✅ 任务完成")
    else:
        print("❌ 任务失败")


if __name__ == "__main__":
    asyncio.run(main())
