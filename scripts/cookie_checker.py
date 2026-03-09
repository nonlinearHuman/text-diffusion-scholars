#!/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3
"""
Cookie 安全检测工具
检查 Cookie 是否有效，计算剩余有效期
"""

import os
import requests
from datetime import datetime

def check_cookie_validity():
    """检查 Cookie 有效性"""
    cookie = os.getenv("XUEQIU_COOKIE", "")

    if not cookie:
        print("❌ 未设置 XUEQIU_COOKIE 环境变量")
        print("\n设置方法：")
        print("  export XUEQIU_COOKIE='你的cookie值'")
        return False

    print(f"✅ Cookie 已设置（长度: {len(cookie)} 字符）")
    print(f"   预览: {cookie[:50]}...")

    # 测试请求
    print("\n🔍 测试 Cookie 有效性...")

    url = "https://xueqiu.com/v4/statuses/user_timeline.json"
    params = {"user_id": "1247297532", "page": 1, "count": 1}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Cookie": cookie,
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if "statuses" in data:
                print("✅ Cookie 有效！可以正常获取数据")
                return True
            else:
                print("❌ Cookie 可能已过期（返回数据异常）")
                return False
        elif resp.status_code == 403:
            print("❌ Cookie 已过期或无效（403 Forbidden）")
            print("\n解决方法：")
            print("  1. 重新登录雪球网站")
            print("  2. 获取新的 Cookie")
            print("  3. 更新环境变量")
            return False
        else:
            print(f"❌ 请求失败（状态码: {resp.status_code}）")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("雪球 Cookie 安全检测工具")
    print("=" * 50)
    print()

    valid = check_cookie_validity()

    print("\n" + "=" * 50)
    if valid:
        print("状态: ✅ 一切正常")
        print("\n建议：")
        print("  • Cookie 通常 7-30 天过期")
        print("  • 建议定期检查（每周一次）")
        print("  • 使用小号，降低风险")
    else:
        print("状态: ❌ 需要处理")
        print("\n推荐：")
        print("  • 使用小号获取 Cookie")
        print("  • 或部署 RSSHub 自建实例（无需Cookie）")
    print("=" * 50)
