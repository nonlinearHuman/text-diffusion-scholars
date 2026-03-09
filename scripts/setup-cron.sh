#!/bin/bash
# 设置雪球日报定时任务（简化版）

PYTHON="/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3"
SCRIPT="/Users/gesong/.openclaw/workspace/scripts/xueqiu_daily.py"
LOG_FILE="/tmp/xueqiu_daily.log"

# 创建定时任务
echo "0 8 * * * $PYTHON $SCRIPT >> $LOG_FILE 2>&1" > /tmp/xueqiu_cron.txt
crontab /tmp/xueqiu_cron.txt

# 验证
echo "✅ 定时任务已设置"
echo ""
echo "📋 当前定时任务："
crontab -l
echo ""
echo "📝 日志文件: $LOG_FILE"
echo ""
echo "🧪 测试运行："
echo "   $PYTHON $SCRIPT"
