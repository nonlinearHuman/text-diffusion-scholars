#!/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3
"""
雪球调试脚本 - 检查页面结构
"""

import asyncio
from playwright.async_api import async_playwright

async def debug_page():
    """调试页面结构"""
    url = "https://xueqiu.com/u/1247297532"
    
    print(f"🎭 启动浏览器调试模式...")
    
    async with async_playwright() as p:
        # 启动浏览器（非无头，方便观察）
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器
            channel='chromium',
            args=[
                '--disable-blink-features=AutomationControlled',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )
        
        page = await context.new_page()
        
        print(f"📡 访问页面: {url}")
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        
        print(f"⏳ 等待页面加载...")
        await page.wait_for_timeout(8000)
        
        # 截图
        screenshot_path = "/Users/gesong/.openclaw/workspace/scripts/xueqiu_debug.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 截图已保存: {screenshot_path}")
        
        # 检查各种可能的选择器
        selectors = [
            ".status-item",
            ".timeline-item",
            ".status-item[data-id]",
            "[class*='status']",
            "[class*='timeline']",
            ".user-status-list .status-item",
            ".status-list .status-item",
        ]
        
        for selector in selectors:
            items = await page.query_selector_all(selector)
            print(f"🔍 {selector}: {len(items)} 个元素")
        
        # 获取页面HTML片段
        html = await page.content()
        print(f"\n📄 页面标题: {await page.title()}")
        print(f"📄 HTML长度: {len(html)} 字符")
        
        # 检查是否有登录提示
        login_check = await page.query_selector(".login-modal, .login-wrapper, [class*='login']")
        if login_check:
            print(f"⚠️  检测到登录提示!")
        
        # 检查是否有验证码
        captcha_check = await page.query_selector("[class*='captcha'], [class*='verify']")
        if captcha_check:
            print(f"⚠️  检测到验证码!")
        
        # 打印页面结构（搜索包含"发言"或"状态"的元素）
        print(f"\n🔍 搜索包含发言内容的元素...")
        content_elements = await page.query_selector_all("div:has-text('大道'), div:has-text('今天'), div:has-text('小时前')")
        print(f"找到 {len(content_elements)} 个可能包含发言的元素")
        
        # 打印第一个元素的HTML
        if content_elements:
            first_elem = content_elements[0]
            outer_html = await first_elem.evaluate("el => el.outerHTML")
            print(f"\n第1个元素HTML预览:\n{outer_html[:500]}...")
        
        print(f"\n按 Ctrl+C 关闭浏览器...")
        await page.wait_for_timeout(30000)  # 等待30秒观察
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_page())
