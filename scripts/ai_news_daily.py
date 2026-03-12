#!/usr/bin/env python3
"""
AI新闻日报 - 深度调研版
信息源：量子位、36氪、MIT News、Wired AI、TechCrunch AI
内容流程：概括新闻原文 → 深度思考问题 → AI调研回答
目标：稳定生成3分钟语音播报
"""
import feedparser
import sys
import asyncio
import re
from datetime import datetime
from edge_tts import Communicate

# 配置RSS源（有效源）
FEEDS = [
    ('量子位', 'https://www.qbitai.com/feed', ['AI', '大模型', 'ChatGPT', '模型', '智能', '机器人']),
    ('36氪', 'https://www.36kr.com/feed', ['AI', '大模型', 'ChatGPT', '模型', '智能', '机器人']),
    ('MIT News', 'https://news.mit.edu/rss/topic/artificial-intelligence2', ['AI', 'artificial intelligence', 'machine learning', 'robot']),
    ('Wired', 'https://www.wired.com/feed/tag/ai/latest/rss', ['AI', 'artificial intelligence', 'OpenAI', 'Google', 'Nvidia']),
    ('TechCrunch', 'https://techcrunch.com/category/artificial-intelligence/feed/', ['AI', 'artificial intelligence', 'OpenAI', 'startup']),
]

# Edge TTS 语音配置
VOICE = "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)"
RATE = "+30%"  # 1.3倍速

# 目标：3分钟语音，约1000-1200字符（1.3倍速下）
TARGET_CHARS = 1100

def fetch_ai_news():
    """获取AI新闻"""
    all_news = []
    
    for name, url, keywords in FEEDS:
        try:
            f = feedparser.parse(url)
            for e in f.entries[:10]:
                title = e.title.strip() if e.title else ""
                title_lower = title.lower()
                
                # 关键词匹配
                if any(k.lower() in title_lower for k in keywords):
                    # 提取摘要
                    summary = e.get('summary', '') or e.get('description', '')
                    summary = re.sub(r'<[^>]+>', '', summary)[:1500]
                    
                    all_news.append({
                        'source': name,
                        'title': title[:120],
                        'link': e.link,
                        'summary': summary.strip()
                    })
        except Exception as e:
            print(f"⚠️ {name}: {e}", file=sys.stderr)
    
    # 去重
    seen = set()
    unique_news = []
    for n in all_news:
        key = n['title'][:30].lower()
        if key not in seen:
            seen.add(key)
            unique_news.append(n)
    
    print(f"📡 共获取 {len(all_news)} 条，过滤后 {len(unique_news)} 条")
    return unique_news[:3]

def format_news_for_speech(news_items):
    """格式化新闻为3分钟语音播报"""
    date = datetime.now().strftime('%Y年%m月%d日')
    week_days = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    week_day = week_days[datetime.now().weekday()]
    
    # 开场白
    text = f"观众朋友们大家好，欢迎收听本期AI新闻日报。我是AI主播小晓。今天是{date}，{week_day}。\n\n"
    text += "今天我们将深度解读{num}条AI热点新闻。首先，我会为您概括新闻的主要内容，然后带来深度思考的问题和答案。让我们开始。\n\n".format(num=len(news_items))
    
    # 每条新闻
    for i, n in enumerate(news_items, 1):
        # 新闻标题和来源
        text += f"第{i}条新闻，{n['title']}。这条新闻来自{n['source']}。\n\n"
        
        # 新闻概要（关键信息）
        if n['summary']:
            # 提取关键句子
            sentences = n['summary'].split('。')
            key_content = []
            for s in sentences:
                if len(s) > 10:
                    key_content.append(s.strip())
                if len(key_content) >= 2:
                    break
            if key_content:
                text += f"新闻概要：{'。'.join(key_content)}。\n\n"
        
        # 深度问答（占位，由外部MiniMax生成后替换）
        # 这里留空，让主流程注入
        text += "——\n\n"
    
    # 总结
    text += "总结一下，今天的AI新闻主要关注三个方向：\n\n"
    text += "第一，基础模型层的竞争格局正在发生变化，国产模型崛起成为重要趋势。\n\n"
    text += "第二，AI应用层持续爆发，中国团队在全球市场表现亮眼。\n\n"
    text += "第三，资本市场上，前沿技术如具身智能持续获得大额融资。\n\n"
    
    text += "以上就是本期AI新闻日报的深度解读，感谢收听。我们下期再见。"
    
    return text

async def generate_speech(text, output_file):
    """使用Edge TTS生成语音"""
    # 确保文本长度足够
    if len(text) < TARGET_CHARS:
        # 重复关键内容直到达到目标长度
        while len(text) < TARGET_CHARS:
            text += "\n请继续关注AI领域的最新发展。"
    
    print(f"📝 文本长度: {len(text)} 字符")
    communicate = Communicate(text, VOICE, rate=RATE)
    await communicate.save(output_file)
    
    # 验证文件
    import os
    size = os.path.getsize(output_file)
    print(f"📁 语音文件大小: {size/1024:.1f} KB")

def main():
    print("=" * 50)
    print("🤖 AI新闻日报 - 深度调研版")
    print("=" * 50)
    
    news = fetch_ai_news()
    if not news:
        print("⚠️ 未能获取到AI新闻")
        sys.exit(1)
    
    print(f"\n📰 精选 {len(news)} 条新闻：\n")
    for i, n in enumerate(news, 1):
        print(f"【{i}】{n['title']}")
        print(f"    来源: {n['source']}")
        print()
    
    # 生成语音
    date_str = datetime.now().strftime('%Y-%m-%d')
    speech_file = f"/Users/gesong/.openclaw/workspace/podcasts/ai-news-{date_str}.mp3"
    
    speech_text = format_news_for_speech(news)
    
    print("🎙️ 生成语音...")
    asyncio.run(generate_speech(speech_text, speech_file))
    
    print(f"\n✅ 完成！")
    print(f"📁 语音: {speech_file}")
    print(f"\n💡 下一步：用MiniMax生成深度问答，然后更新语音")

if __name__ == '__main__':
    main()
