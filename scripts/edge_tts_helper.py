#!/usr/bin/env python3
"""
Edge TTS 中文语音合成工具
"""
import asyncio
from edge_tts import Communicate
import sys
import os

# 可用中文语音
VOICES = {
    "xiaoxiao": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)",  # 女声，温柔
    "xiaoyi": "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoyiNeural)",      # 女声，活泼
    "yunjian": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunjianNeural)",    # 男声，激情
    "yunxi": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunxiNeural)",        # 男声，活泼
    "yunxia": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunxiaNeural)",      # 男声，可爱
    "yunyang": "Microsoft Server Speech Text to Speech Voice (zh-CN, YunyangNeural)",   # 男声，专业
}

def generate_speech(text, output_file, voice_key="xiaoxiao", rate="+0%", volume="+0%", pitch="+0Hz"):
    """生成语音"""
    voice = VOICES.get(voice_key, VOICES["xiaoxiao"])
    
    async def main():
        communicate = Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
        await communicate.save(output_file)
    
    asyncio.run(main())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python edge_tts.py <文本> <输出文件> [语音]")
        print("语音: xiaoxiao(默认), xiaoyi, yunjian, yunxi, yunxia, yunyang")
        sys.exit(1)
    
    text = sys.argv[1]
    output = sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else "xiaoxiao"
    
    generate_speech(text, output, voice)
    print(f"已生成: {output}")
