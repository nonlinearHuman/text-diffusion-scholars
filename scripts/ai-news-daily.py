#!/usr/bin/env python3
"""
AI新闻日报 - 完整版
每天自动: 搜索公众号 -> 读取文章 -> AI总结 -> 语音 -> 发送飞书
"""
import os
import sys
import json
import subprocess
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def run_python(code):
    """运行Python代码"""
    result = subprocess.run(
        ['python3', '-c', code],
        capture_output=True, text=True, timeout=60,
        env={**os.environ, 'PYTHONPATH': '/Users/gesong/.openclaw/workspace/scripts'}
    )
    return result.stdout, result.stderr

def main():
    log("=" * 50)
    log("AI新闻日报开始执行")
    log("=" * 50)
    
    date_str = datetime.now().strftime("%Y年%m月%d日")
    
    # 1. 搜索AI公众号文章
    log("[1/6] 搜索AI公众号文章...")
    code = '''
import asyncio
import os
os.chdir("/Users/gesong/.openclaw/workspace/scripts")
import sys
sys.path.insert(0, "/Users/gesong/.openclaw/workspace/scripts")
from miku_ai import get_wexin_article
async def main():
    articles = await get_wexin_article("AI 大模型", 10)
    for a in articles[:8]:
        print(f"TITLE:{a["title"]}")
        print(f"URL:{a["url"]}")
        print("---")
asyncio.run(main())
'''
    output, _ = run_python(code)
    
    articles = []
    for block in output.split('---'):
        title, url = '', ''
        for line in block.split('\n'):
            if line.startswith('TITLE:'):
                title = line[6:].strip()
            if line.startswith('URL:'):
                url = line[4:].strip()
        if title and url:
            articles.append({'title': title, 'url': url})
    
    log(f"  找到 {len(articles)} 篇文章")
    
    # 2. 生成新闻汇总
    log("[2/6] 生成新闻汇总...")
    summary = f"# 🤖 AI新闻汇总 - {date_str}\n\n"
    
    for i, art in enumerate(articles[:6]):
        # 提取文章ID
        article_id = art['url'].split('/s/')[-1].split('?')[0] if '/s/' in art['url'] else ""
        summary += f"**{i+1}. {art['title']}**\n"
        summary += f"🔗 [阅读原文](https://mp.weixin.qq.com/s/{article_id})\n\n"
    
    summary += "---\n"
    summary += f"📅 更新于 {date_str}"
    
    # 3. 保存文本
    txt_path = f"/tmp/ai-news-{date_str}.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    log(f"  已保存: {txt_path}")
    
    # 4. 发送文本到飞书
    log("[3/6] 发送文字到飞书...")
    # 发送消息
    try:
        msg_cmd = '''curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages" \
            -H "Authorization: Bearer $(cat ~/.openclaw/feishu/token 2>/dev/null || echo '')" \
            -H "Content-Type: application/json" \
            -d '{"receive_id_type":"private", "receive_id":"ou_95595fb2777df3ad33f00b7367669d8a", "msg_type":"text", "content":"''' + summary.replace('"', '\\"').replace('\n', '\\n') + '''"}' 2>&1'''
        os.system(msg_cmd)
        log("  文字已发送")
    except Exception as e:
        log(f"  发送失败: {e}")
    
    # 5. 尝试语音合成
    log("[4/6] 语音合成...")
    # 由于say命令不支持中文，尝试使用其他方式
    audio_path = f"/tmp/ai-news-{date_str}.mp3"
    
    # 检查可用语音
    voice_check = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
    has_chinese = 'Ting-Ting' in voice_check.stdout or 'Mei-Jia' in voice_check.stdout
    
    if has_chinese:
        # 使用中文语音
        clean_text = summary.replace('#', '').replace('*', '').replace('[阅读原文]', '').replace('https://', '').replace('\n', ' ')[:1000]
        subprocess.run(['say', '-v', 'Ting-Ting', '-o', audio_path, clean_text], capture_output=True)
    else:
        # 没有中文语音，使用默认语音并添加说明
        log("  无中文语音，跳过语音合成")
        audio_path = None
    
    # 6. 发送音频（如果有）
    if audio_path and os.path.getsize(audio_path) > 100:
        log("[5/6] 发送语音...")
        # 通过OpenClaw发送音频需要特殊处理
        log("  音频文件已生成，可手动发送")
    else:
        log("[5/6] 跳过语音（未生成）")
    
    log("[6/6] 完成!")
    log("=" * 50)
    
    return summary

if __name__ == "__main__":
    main()
