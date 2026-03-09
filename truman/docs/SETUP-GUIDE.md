# 楚门项目配置指南

## ✅ 已完成
- [x] 安装依赖（淘宝镜像）
- [x] 创建 .env 配置文件
- [x] 生成加密密钥

## 🔧 待完成

### 1. 创建 Discord Bot

#### 步骤：

1. **访问 Discord Developer Portal**
   - 打开：https://discord.com/developers/applications
   - 登录你的 Discord 账号

2. **创建新应用**
   - 点击 "New Application"
   - 名称填写：`Truman` 或 `楚门`
   - 点击 Create

3. **创建 Bot 用户**
   - 左侧菜单选择 "Bot"
   - 点击 "Add Bot"
   - 确认创建

4. **获取 Token**
   - 在 Bot 页面，点击 "Reset Token"
   - 复制生成的 Token（只显示一次！）
   - 粘贴到 `.env` 文件的 `DISCORD_TOKEN`

5. **获取 Client ID**
   - 左侧菜单选择 "General Information"
   - 复制 "APPLICATION ID"
   - 粘贴到 `.env` 文件的 `DISCORD_CLIENT_ID`

6. **获取 Server ID**
   - 打开 Discord 客户端
   - 进入你的服务器（或创建一个测试服务器）
   - 右键服务器名称 → "复制 ID"
   - 粘贴到 `.env` 文件的 `DISCORD_GUILD_ID`

7. **邀请 Bot 到服务器**
   - 左侧菜单选择 "OAuth2" → "URL Generator"
   - 勾选权限：
     - `bot`
     - `applications.commands`
   - Bot Permissions 勾选：
     - Send Messages
     - Manage Messages
     - Read Message History
     - Use Slash Commands
   - 复制生成的 URL，浏览器打开，授权 Bot 加入服务器

---

### 2. 部署 PostgreSQL 数据库（Railway 推荐）

#### 方法一：Railway（免费额度足够）

1. **注册 Railway**
   - 访问：https://railway.app
   - 用 GitHub 登录

2. **创建数据库**
   - 点击 "+ New Project"
   - 选择 "Provision PostgreSQL"
   - 等待创建完成（约 10 秒）

3. **获取连接 URL**
   - 点击 PostgreSQL 项目
   - 选择 "Variables" 标签
   - 复制 `DATABASE_URL`
   - 粘贴到 `.env` 文件

#### 方法二：本地 Docker（如果你有 Docker）

```bash
# 启动 PostgreSQL 容器
docker run --name truman-postgres \
  -e POSTGRES_PASSWORD=truman123 \
  -e POSTGRES_DB=truman \
  -p 5432:5432 \
  -d postgres:15

# 连接 URL
DATABASE_URL=postgresql://postgres:truman123@localhost:5432/truman
```

#### 方法三：Neon（免费，无需信用卡）

1. 访问：https://neon.tech
2. 注册并创建项目
3. 复制 Connection String
4. 粘贴到 `.env` 文件

---

### 3. 初始化数据库

```bash
cd /Users/gesong/.openclaw/workspace/truman
npm run db:migrate
```

---

### 4. 启动 Bot

```bash
npm start
```

或开发模式：

```bash
npm run dev
```

---

## 📝 配置文件示例

`.env` 文件应该像这样：

```bash
# Discord Configuration
DISCORD_TOKEN=MTk4NjIyNDgzNDcOTY3NjI1MjQ.Dk12-3.qWertyuiopasdfghjklzxcvbnm
DISCORD_CLIENT_ID=198622483456762524
DISCORD_GUILD_ID=123456789012345678

# Database Configuration
DATABASE_URL=postgresql://postgres:password@monorail.proxy.rlwy.net:5432/railway

# OpenClaw Configuration
OPENCLAW_API_KEY=c25ece9106f117f7546d22e391c2140c81c591c0856e690e

# Encryption
ENCRYPTION_KEY=e4a9ff4d411736cd2233e5e9042aacfbf1d0ea6cb5872b694cc6df729d00bb26

# Environment
NODE_ENV=development
PORT=3000
```

---

## ⚡ 快速检查清单

完成以上步骤后，运行：

```bash
# 检查依赖
ls node_modules

# 检查配置
cat .env

# 测试数据库连接
node -e "const { Pool } = require('pg'); const pool = new Pool({connectionString: process.env.DATABASE_URL}); pool.query('SELECT NOW()', (err, res) => { console.log(err || '数据库连接成功'); pool.end(); })"

# 启动 Bot
npm start
```

---

## 🆘 常见问题

### Q: Discord Token 在哪里？
A: Discord Developer Portal → 你的应用 → Bot → Reset Token

### Q: 数据库连接失败？
A: 检查 DATABASE_URL 格式，确保是 `postgresql://` 开头

### Q: Bot 无法发送消息？
A: 检查 Bot 权限，确保有 "Send Messages" 权限

### Q: 如何测试 Agent？
A: Bot 启动后，在 Discord 服务器输入 `/agent_test`

---

**准备好后告诉我，我帮你启动项目！**
