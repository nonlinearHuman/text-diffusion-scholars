# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Obsidian

- **Vault 路径**: `~/Documents/obsidian/Xun/`
- **收藏目录**: `Inbox/Clips/`
- **论文推荐输出**: `Inbox/论文推荐/`
- **模板路径**: `Templates/论文技术线索演示文稿生成模板.md`
- **结构**:
  - `Inbox/Clips/小红书/` - 小红书收藏
  - `Inbox/Clips/微博/` - 微博收藏
  - `Inbox/Clips/公众号/` - 公众号收藏
  - `Inbox/Clips/网页/` - 通用网页收藏
  - `Inbox/论文推荐/` - 论文推荐PDF输出
  - `Templates/` - 工作流模板

## 论文推荐工作流

**执行前必须读取模板：**
```
~/Documents/obsidian/Xun/Templates/论文技术线索演示文稿生成模板.md
```

**布局规范：**
- 页面尺寸：254mm × 143mm (PPT 16:9)
- 左侧：76mm (30%) - 作者信息
- 右侧：178mm (70%) - 论文内容

**必填内容：**
- 作者真实照片
- 论文原图
- 近两年代表论文列表

**输出：**
- PDF → `Inbox/论文推荐/{会议名称}-{主题}-推荐.pdf`
- 发送到飞书

---

## 外部服务调用

**配置文件**: `scripts/services.json` - 所有 API Key 和服务端点统一管理

### AI 调用
```bash
# 智谱 GLM (已配置)
python scripts/ai-call.py zhipu "你的提示词"

# DeepSeek (性价比高，适合文案生成)
export DEEPSEEK_API_KEY=your_key
python scripts/ai-call.py deepseek "写一个小红书文案"

# OpenAI
export OPENAI_API_KEY=sk-xxx
python scripts/ai-call.py openai "你的提示词"
```

### 消息推送
```bash
# 飞书 (已配置，直接对话即可)
# 通过 OpenClaw 直接发送消息

# Telegram (需配置)
export TELEGRAM_BOT_TOKEN=xxx
export TELEGRAM_CHAT_ID=xxx
python scripts/notify.py telegram "交易信号：买入 XXX"

# Webhook (企业微信、钉钉等)
export WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
python scripts/notify.py webhook "消息内容"
```

### 股票数据
```python
# 已安装 akshare，直接使用
import akshare as ak
df = ak.stock_zh_a_spot_em()  # A股实时行情
```

---

## 雪球日报（定时任务）

**功能**：
- 每天早上8点抓取"大道无形我有型"（段永平）发言
- 推送到飞书
- 自动归档到 Obsidian `archives/` 文件夹

**方案选择**（推荐 RSSHub 自建）：

### 方案一：RSSHub 自建（推荐）
- ✅ 无需Cookie，永久稳定
- ✅ Docker 一键部署：`docker run -d -p 1200:1200 diygod/rsshub`
- ✅ 脚本：`scripts/xueqiu_rsshub.py`
- 📖 详细指南：`scripts/部署RSSHub指南.md`

### 方案二：Cookie（备选）
- ⚠️ Cookie会过期（7-30天），需定期更新
- ⚠️ 建议用小号，降低风险
- ✅ 脚本：`scripts/xueqiu_daily.py`
- 🔍 检查工具：`scripts/cookie_checker.py`

**方案对比**：`scripts/雪球日报-方案对比.md`

**脚本位置**：`scripts/xueqiu_daily.py`

**配置Cookie**：
```bash
# 方式1：环境变量
export XUEQIU_COOKIE="你的cookie值"

# 方式2：配置文件
nano scripts/.env.xueqiu
# 填入 XUEQIU_COOKIE="..."
```

**安装定时任务**：
```bash
scripts/cron-setup.sh
```

**测试归档**：
```bash
# 查看示例归档（无需Cookie）
scripts/test_archive.py
```

**安装定时任务**：
```bash
scripts/cron-setup.sh
```

**详细文档**：`scripts/雪球日报使用指南.md`

---

Add whatever helps you do your job. This is your cheat sheet.
