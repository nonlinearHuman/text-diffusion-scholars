#!/bin/bash
# 雪球日报定时任务安装脚本

SCRIPT_DIR="/Users/gesong/.openclaw/workspace/scripts"
PYTHON="/Users/gesong/.openclaw/workspace/scripts/venv/bin/python3"
SCRIPT="$SCRIPT_DIR/xueqiu_daily.py"
LOG_FILE="/tmp/xueqiu_daily.log"

# 检查脚本是否存在
if [ ! -f "$SCRIPT" ]; then
    echo "❌ 脚本不存在: $SCRIPT"
    exit 1
fi

# 检查Python环境
if [ ! -f "$PYTHON" ]; then
    echo "❌ Python环境不存在: $PYTHON"
    exit 1
fi

# 添加到 crontab
CRON_JOB="0 8 * * * $PYTHON $SCRIPT >> $LOG_FILE 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "xueqiu_daily.py"; then
    echo "⚠️  定时任务已存在，跳过安装"
    echo ""
    echo "当前任务："
    crontab -l | grep "xueqiu_daily.py"
else
    # 添加任务
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ 定时任务已添加"
    echo ""
    echo "任务内容："
    echo "$CRON_JOB"
fi

echo ""
echo "📋 查看所有定时任务："
echo "   crontab -l"
echo ""
echo "📝 查看日志："
echo "   tail -f $LOG_FILE"
echo ""
echo "🗑️  删除任务："
echo "   crontab -e"
echo "   # 删除包含 xueqiu_daily.py 的那一行"
