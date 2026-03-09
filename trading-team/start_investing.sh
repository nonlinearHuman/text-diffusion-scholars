#!/bin/bash
# 量化投资系统 - 每日启动脚本

cd /Users/gesong/.openclaw/workspace/trading-team
source venv/bin/activate

echo "🚀 启动量化投资系统..."
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 运行分析
python quant_investor.py

# 可选：发送到飞书（需要配置）
# python send_to_feishu.py
