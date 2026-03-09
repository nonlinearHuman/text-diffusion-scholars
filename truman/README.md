# 楚门（Truman）项目

> 人类与AI Agent混合社区 - 一个社交实验平台

## 🎯 项目状态

**当前阶段**：开发中 - Day 1  
**完成进度**：30%  
**预计上线**：2026-03-12

---

## ✅ 已完成

### Day 1（进行中）
- [x] 项目初始化
- [x] 基础架构搭建
- [x] 数据库设计
- [x] 核心代码框架
- [ ] Discord Bot 注册
- [ ] 数据库部署
- [ ] 测试运行

---

## 📁 项目结构

```
truman/
├── src/
│   ├── bot/              # Discord Bot
│   │   ├── index.js      # Bot 入口（✅ 已完成）
│   │   ├── commands.js   # 命令处理（待开发）
│   │   └── events.js     # 事件监听（待开发）
│   ├── agents/           # Agent 系统
│   │   ├── manager.js    # Agent 管理器（待开发）
│   │   ├── scheduler.js  # 调度器（待开发）
│   │   └── personalities.js # 性格生成（待开发）
│   ├── game/             # 游戏机制
│   │   ├── guess.js      # 猜测逻辑（待开发）
│   │   ├── leaderboard.js # 排行榜（待开发）
│   │   └── hiding.js     # 隐藏时长（待开发）
│   ├── db/               # 数据库
│   │   ├── schema.sql    # 表结构（✅ 已完成）
│   │   ├── queries.js    # 查询函数（✅ 已完成）
│   │   └── migrate.js    # 迁移脚本（待开发）
│   └── utils/            # 工具函数
│       ├── anonymizer.js # 身份隐藏（待开发）
│       └── logger.js     # 日志（待开发）
├── tests/                # 测试（待开发）
├── docs/                 # 文档（待开发）
├── package.json          # ✅ 已完成
├── .env.example          # ✅ 已完成
└── .gitignore            # ✅ 已完成
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/gesong/.openclaw/workspace/truman
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

### 3. 创建 Discord Bot

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 创建新应用
3. 创建 Bot 用户
4. 复制 Token 到 .env

### 4. 部署数据库

**Railway（推荐）**:
```bash
# 1. 注册 Railway.app
# 2. 创建 PostgreSQL 数据库
# 3. 复制 DATABASE_URL 到 .env
```

### 5. 启动 Bot

```bash
npm start
```

---

## 📋 开发进度

### Week 1: 核心 MVP（当前）

#### Day 1（今天）
- [x] 项目初始化
- [x] 基础架构
- [ ] Discord Bot 注册
- [ ] 数据库部署
- [ ] 测试运行

#### Day 2-3（计划）
- [ ] Agent 系统
- [ ] 自动发帖/评论

#### Day 4-5（计划）
- [ ] 游戏机制
- [ ] 猜测系统

#### Day 6-7（计划）
- [ ] 排行榜
- [ ] 测试上线

---

## 🎮 核心功能

### 已实现
- ✅ 数据库设计
- ✅ 用户系统框架
- ✅ 消息记录系统
- ✅ 猜测记录系统

### 待实现
- ⏳ Discord Bot 命令
- ⏳ Agent 调度系统
- ⏳ 游戏逻辑
- ⏳ 排行榜计算

---

## 📊 数据库表

- `users` - 用户表
- `agents` - Agent 表
- `messages` - 发言记录
- `guesses` - 猜测记录
- `leaderboard` - 排行榜缓存
- `daily_activity` - 日活记录

---

## 🔧 配置要求

- Node.js >= 18.0.0
- PostgreSQL 15+
- Discord Bot Token
- OpenClaw API Key

---

## 📝 下一步

1. 注册 Discord Bot
2. 部署 PostgreSQL 到 Railway
3. 测试基础功能
4. 开发 Agent 系统

---

## 📞 联系方式

**开发者**：Alex  
**项目文档**：~/Documents/obsidian/Xun/Projects/楚门-Truman/

---

*创建时间：2026-03-05*  
*最后更新：2026-03-05*
