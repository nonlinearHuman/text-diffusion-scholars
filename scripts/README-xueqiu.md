# 雪球定时任务配置说明

## 方式一：OpenClaw Cron（推荐）

OpenClaw 支持内置 cron 定时任务。

### 配置步骤：

1. 在项目根目录创建 `cron.json`：

```json
{
  "jobs": [
    {
      "id": "xueqiu-daily",
      "schedule": "0 8 * * *",
      "command": "python3 /Users/gesong/.openclaw/workspace/scripts/xueqiu_daily.py",
      "timezone": "Asia/Shanghai",
      "enabled": true
    }
  ]
}
```

2. 重启 OpenClaw Gateway：

```bash
openclaw gateway restart
```

3. 查看任务状态：

```bash
openclaw gateway status
```

---

## 方式二：系统 crontab（备选）

### 配置步骤：

1. 编辑 crontab：

```bash
crontab -e
```

2. 添加任务：

```bash
# 每天早上8点执行雪球日报
0 8 * * * /usr/bin/python3 /Users/gesong/.openclaw/workspace/scripts/xueqiu_daily.py >> /tmp/xueqiu_daily.log 2>&1
```

3. 保存退出

4. 查看任务：

```bash
crontab -l
```

---

## 方式三：launchd（macOS 原生）

### 配置步骤：

1. 创建 plist 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.xueqiu</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/gesong/.openclaw/workspace/scripts/xueqiu_daily.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/xueqiu_daily.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/xueqiu_daily.error.log</string>
</dict>
</plist>
```

2. 保存为 `~/Library/LaunchAgents/com.openclaw.xueqiu.plist`

3. 加载任务：

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.xueqiu.plist
```

---

## 🍪 获取雪球 Cookie（重要）

雪球API需要登录Cookie才能访问。

### 获取步骤：

1. 打开浏览器，访问 https://xueqiu.com
2. 登录你的雪球账号
3. 按 F12 打开开发者工具
4. 切换到 "Network" 标签
5. 刷新页面
6. 找到任意请求，查看 Request Headers
7. 复制 Cookie 字段的值

### 配置Cookie：

```bash
# 方式1：设置环境变量
export XUEQIU_COOKIE="你的cookie值"

# 方式2：写入 .env 文件
echo 'XUEQIU_COOKIE="你的cookie值"' >> ~/.openclaw/workspace/scripts/.env
```

---

## 📝 测试任务

手动执行测试：

```bash
python3 /Users/gesong/.openclaw/workspace/scripts/xueqiu_daily.py
```

---

## 📊 查看日志

- OpenClaw cron: `tail -f ~/.openclaw/logs/cron.log`
- 系统 cron: `tail -f /tmp/xueqiu_daily.log`
- launchd: `tail -f /tmp/xueqiu_daily.log`

---

## ⚠️ 注意事项

1. **Cookie 有效期**：雪球 Cookie 可能过期，需要定期更新
2. **用户ID**：当前配置的是"大道无形我有型"（1247297532）
3. **时区**：确保服务器时区为 Asia/Shanghai
4. **网络**：确保服务器能访问 xueqiu.com

---

## 🔧 自定义配置

修改 `xueqiu_tracker.py` 中的 CONFIG：

```python
CONFIG = {
    "user_id": "1247297532",  # 修改为其他用户ID
    "username": "大道无形我有型",
    "api_url": "https://xueqiu.com/v4/statuses/user_timeline.json",
}
```

---

**配置好后告诉我，我帮你启动定时任务！**
