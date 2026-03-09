#!/bin/bash
# 快速反馈脚本 - 用户执行交易后反馈

cd /Users/gesong/.openclaw/workspace/trading-team
source venv/bin/activate

echo "📝 交易反馈录入"
echo "=================="
echo ""
echo "格式："
echo "  BUY 000001 平安银行 10.01 100"
echo "  SELL 000001 平安银行 10.50 100"
echo "  STATUS 1000  # 更新账户现金"
echo ""
echo "示例："
echo "  ✅ 买入成功：BUY 000001 平安银行 10.01 100"
echo "  ✅ 卖出成功：SELL 000001 平安银行 10.50 100"
echo "  ❌ 未执行：NO"
echo ""

python trading_assistant.py
