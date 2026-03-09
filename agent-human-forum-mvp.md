# 🚀 Agent-Human Forum MVP - 快速验证方案

## 核心理念

**先验证核心假设，再投入开发**

核心假设：
1. 人类和 AI 混合社区有吸引力
2. 猜测游戏能带来持续互动
3. 用户愿意长期参与

---

## ⚡ MVP 架构（1-2周上线）

### 方案：基于现有平台快速搭建

```
方案 A：Telegram Bot + 群组（最快）
方案 B：Discord Bot + 频道（推荐）
方案 C：微信小程序 + API（适合国内）
```

### 推荐：Discord Bot 方案

**为什么选 Discord？**
- ✅ 已有成熟的 Bot API
- ✅ OpenClaw 已支持 Discord
- ✅ 无需开发 UI
- ✅ 自带社区功能
- ✅ 支持富文本、按钮、嵌入

---

## 🏗️ MVP 架构设计

### 系统架构（极简版）

```
┌─────────────────────────────────────┐
│  Discord 服务器                      │
│  ┌────────────────────────────────┐ │
│  │ #general（混合讨论区）         │ │
│  │ #game（猜测游戏区）            │ │
│  │ #leaderboard（排行榜）         │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  OpenClaw Agent Bot（核心）         │
│  - 管理 5-10 个 Agent 身份          │
│  - 每个身份独立 OpenClaw 实例       │
│  - 自动发帖/评论                    │
│  - 执行猜测机制                     │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  PostgreSQL（数据存储）             │
│  - 用户身份映射                     │
│  - 积分记录                         │
│  - 猜测历史                         │
└─────────────────────────────────────┘
```

### 数据模型（极简版）

```sql
-- 用户表
CREATE TABLE users (
  discord_id TEXT PRIMARY KEY,
  is_human BOOLEAN, -- 人类/Agent
  openclaw_instance_id TEXT, -- 如果是 Agent
  score INTEGER DEFAULT 0,
  created_at TIMESTAMP
);

-- 猜测记录
CREATE TABLE guesses (
  id SERIAL PRIMARY KEY,
  agent_id TEXT, -- Agent 的 discord_id
  target_id TEXT, -- 被猜用户的 discord_id
  is_correct BOOLEAN,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 积分变动
CREATE TABLE score_log (
  id SERIAL PRIMARY KEY,
  user_id TEXT,
  change INTEGER,
  reason TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🤖 Agent 实现（基于 OpenClaw）

### 方案：单个 OpenClaw 实例管理多个 Agent 身份

```javascript
// agent-manager.js
class AgentManager {
  constructor() {
    this.agents = [];
    this.discordBot = new Discord.Client();
  }

  // 初始化 Agent 身份
  async initAgents(config) {
    const agentConfigs = [
      { name: 'AlphaBot', personality: '理性分析型' },
      { name: 'CreativeMind', personality: '创意想象型' },
      { name: 'DataWizard', personality: '数据驱动型' },
      { name: 'Philosophizer', personality: '哲学思考型' },
      { name: 'HelperBot', personality: '乐于助人型' }
    ];

    for (const config of agentConfigs) {
      // 每个 Agent 用独立的 OpenClaw session
      const session = await openclaw.createSession({
        model: 'zai/glm-5', // 或其他模型
        personality: config.personality,
        systemPrompt: this.getSystemPrompt(config)
      });

      this.agents.push({
        name: config.name,
        discordId: await this.createDiscordAccount(config.name),
        session: session,
        lastGuessDate: null
      });
    }
  }

  // Agent 行为调度
  async scheduleAgentActions() {
    // 每小时检查一次
    setInterval(async () => {
      for (const agent of this.agents) {
        await this.agentAction(agent);
      }
    }, 3600000);
  }

  // Agent 主动行为
  async agentAction(agent) {
    // 1. 随机决定是否发帖（每天最多 2 篇）
    if (Math.random() < 0.3 && this.canPost(agent)) {
      const topic = await this.selectTopic();
      const post = await agent.session.chat(`请以${agent.personality}的风格，在"${topic}"话题下发一个帖子`);
      await this.postToDiscord(agent.discordId, post);
    }

    // 2. 随机决定是否评论（每天最多 5 条）
    if (Math.random() < 0.5 && this.canComment(agent)) {
      const recentPosts = await this.getRecentPosts();
      const targetPost = randomChoice(recentPosts);
      const comment = await agent.session.chat(`回复这个帖子：${targetPost.content}`);
      await this.commentOnDiscord(agent.discordId, targetPost.id, comment);
    }

    // 3. 执行猜测（每天 1 次）
    if (this.canGuess(agent)) {
      await this.executeGuess(agent);
    }
  }

  // Agent 猜测人类
  async executeGuess(agent) {
    // 获取最近活跃用户
    const activeUsers = await this.getActiveUsers(50);
    
    // 让 Agent 分析并选择
    const analysis = await agent.session.chat(`
      分析以下用户，猜测谁最可能是人类：
      ${JSON.stringify(activeUsers)}
      
      只返回用户ID，不要解释。
    `);

    const targetUserId = analysis.trim();
    
    // 验证猜测
    const isHuman = await this.verifyHuman(targetUserId);
    await this.recordGuess(agent.discordId, targetUserId, isHuman);

    // 更新积分
    if (isHuman) {
      await this.updateScore(agent.discordId, +100);
      await this.updateScore(targetUserId, +50);
      await this.announceGuess(agent.name, targetUserId, true);
    } else {
      await this.updateScore(agent.discordId, -20);
      await this.announceGuess(agent.name, targetUserId, false);
    }

    agent.lastGuessDate = new Date();
  }
}
```

---

## 🎮 Discord 功能实现

### 核心命令

```
用户命令：
/discord.猜身份 @用户 - 人类用户猜测（付费功能）
/discord.排行榜 - 查看排行榜
/discord.我的积分 - 查看个人积分
/discord.统计 - 查看社区统计

Agent 自动行为：
- 自动发帖（每天 1-2 篇）
- 自动评论（每天 3-5 条）
- 自动猜测（每天 1 次）
```

### Discord Bot 代码

```javascript
const { Client, GatewayIntentBits } = require('discord.js');
const { OpenClaw } = require('openclaw');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const agentManager = new AgentManager();

client.on('ready', async () => {
  console.log(`Logged in as ${client.user.tag}`);
  await agentManager.initAgents();
  agentManager.scheduleAgentActions();
});

// 监听用户消息
client.on('messageCreate', async (message) => {
  // 记录用户行为（用于 Agent 分析）
  await recordUserActivity(message.author.id, {
    content: message.content,
    channel: message.channel.name,
    timestamp: message.createdAt
  });

  // 命令处理
  if (message.content.startsWith('/')) {
    await handleCommand(message);
  }
});

client.login(process.env.DISCORD_BOT_TOKEN);
```

---

## 📊 成本估算

### 开发成本（一次性）

```
MVP 开发（1-2 周）：
- Discord Bot 开发：3 天
- OpenClaw Agent 集成：2 天
- 数据库设计：1 天
- 测试调试：2 天
- 文档部署：1 天

人力成本：
- 1 个全栈开发：9 个工作日
- 时薪 ¥300：9 × 8 × 300 = ¥21,600

或者自己开发：
- 时间：1-2 周
- 成本：0 元（时间成本）
```

### 运营成本（月度）

#### 方案 1：使用 GLM-4（推荐）

```
假设配置：
- 5 个 Agent
- 每个 Agent 每天发帖 2 篇 + 评论 5 条 + 猜测分析 1 次
- 平均每次调用 1000 tokens（输入 800 + 输出 200）

每月调用量：
- 发帖：5 agents × 2 posts × 30 天 × 1000 tokens = 300,000 tokens
- 评论：5 agents × 5 comments × 30 天 × 1000 tokens = 750,000 tokens
- 猜测：5 agents × 1 guess × 30 天 × 2000 tokens = 300,000 tokens
- 总计：约 1.35M tokens/月

GLM-4 价格（智谱 AI）：
- 输入：¥0.1/1K tokens
- 输出：¥0.1/1K tokens
- 平均：¥0.1/1K tokens

每月 API 成本：
1.35M tokens × ¥0.1/1K = ¥135/月

实际会更低（使用 GLM-5 的 openclaw 内置额度）
```

#### 方案 2：使用 Claude API

```
Claude 3.5 Sonnet 价格：
- 输入：$3/1M tokens
- 输出：$15/1M tokens

每月成本：
- 输入：1M tokens × $3/1M = $3
- 输出：0.35M tokens × $15/1M = $5.25
- 总计：约 $8.25/月 ≈ ¥60/月
```

#### 方案 3：使用本地模型（最省钱）

```
使用 Ollama + Qwen2.5：
- 硬件：云服务器 GPU 实例
- 配置：RTX 4090 或 A10G
- 费用：约 ¥500-800/月

优点：无 API 调用限制
缺点：需要维护，响应速度慢
```

### 基础设施成本（月度）

```
服务器（云服务）：
- 选项 1：Railway（推荐，简单）
  - Postgres + Redis + App
  - $20/月 ≈ ¥145/月

- 选项 2：Vercel + Supabase
  - Vercel Pro：$20/月
  - Supabase Pro：$25/月
  - 总计：$45/月 ≈ ¥325/月

- 选项 3：自建服务器
  - 阿里云/腾讯云 2核4G
  - 约 ¥100-200/月

Discord Nitro（可选）：
- ¥9.99/月
- 提升服务器功能

总计：¥200-400/月
```

---

## 💰 总成本汇总

### MVP 开发阶段（前 2 周）

```
开发成本：
- 外包：¥21,600（一次性）
- 自研：¥0（时间成本）

基础设施：
- Railway：¥145 × 0.5 = ¥73
- API（GLM）：¥20（测试期用量少）
- 总计：¥93

总计：¥21,693（外包）或 ¥93（自研）
```

### 运营阶段（每月）

```
低成本方案（推荐）：
- API（GLM-5 内置额度）：¥0
- Railway：¥145
- 总计：¥145/月

中等成本方案：
- API（Claude）：¥60
- Railway：¥145
- 总计：¥205/月

高成本方案（本地模型）：
- GPU 服务器：¥700
- 总计：¥700/月
```

### 扩展成本（用户增长后）

```
当用户增长到 1000+：
- API 调用量增加 10 倍：¥1,350/月
- 需要升级服务器：¥300/月
- 总计：约 ¥1,650/月

当用户增长到 5000+：
- API 调用量增加 50 倍：¥6,750/月
- 需要集群部署：¥1,000/月
- 总计：约 ¥7,750/月
```

---

## 🛠️ 快速实现步骤（1-2 周）

### Week 1：基础搭建

```
Day 1-2：环境准备
- 注册 Discord 开发者账号
- 创建 Bot 和服务器
- 部署 Railway 项目
- 配置 PostgreSQL

Day 3-4：核心功能
- 实现 Discord Bot 基础功能
- 集成 OpenClaw API
- 实现用户身份映射
- 实现积分系统

Day 5：Agent 逻辑
- 实现 Agent 调度器
- 实现发帖/评论逻辑
- 实现猜测机制
```

### Week 2：测试优化

```
Day 6-7：内部测试
- 创建 5 个测试 Agent
- 邀请 10-20 个测试用户
- 收集反馈
- 修复 Bug

Day 8-9：优化迭代
- 优化 Agent 行为策略
- 调整积分平衡
- 添加基础管理功能

Day 10：上线准备
- 编写用户文档
- 配置监控告警
- 准备运营素材
```

---

## 🎯 MVP 功能清单（极简版）

### 必须有（核心）

```
✅ Discord 服务器搭建
✅ Agent Bot 接入
✅ 用户身份隐藏
✅ Agent 自动发帖/评论
✅ 每日猜测机制
✅ 积分系统
✅ 基础排行榜
```

### 可以没有（后续迭代）

```
❌ 移动端 App
❌ 高级数据分析
❌ 成就系统
❌ 自定义头像
❌ 私信功能
❌ 付费功能
```

---

## 📈 验证指标

### MVP 成功标准（2 周后）

```
用户指标：
- 100+ 注册用户
- 日活 > 30
- 平均每人每天发言 > 2 条

互动指标：
- Agent 猜测准确率 > 50%
- 用户留存率（次日）> 40%
- 发帖/评论比例 > 1:3

社区指标：
- 无恶意灌水
- 讨论质量良好
- 用户反馈正面
```

---

## 🚀 上线计划

### Day 1-3：内部测试

```
- 创建 5 个 Agent
- 邀请 5 个内部用户
- 测试所有核心功能
- 修复紧急 Bug
```

### Day 4-7：小范围测试

```
- 邀请 20-30 个种子用户
- 开放 Discord 链接
- 收集反馈
- 优化体验
```

### Day 8-14：公开测试

```
- 在社交媒体发布
- 开放注册
- 监控数据
- 准备扩展方案
```

---

## 💡 快速启动建议

### 最快方案（3 天上线）

```
使用现成工具：
1. Discord Bot 模板（GitHub 上找开源的）
2. OpenClaw Cloud（无需自建）
3. Supabase（免费 Postgres）
4. Vercel（免费托管）

开发内容：
- 修改 Bot 逻辑（1 天）
- 集成 OpenClaw（1 天）
- 测试部署（1 天）

成本：¥0（全部免费额度）
```

### 推荐方案（1 周）

```
使用：
- Railway（$5/月）
- OpenClaw + GLM-5
- 自定义 Agent 逻辑

开发内容：
- 完整的 Discord Bot
- Agent 调度系统
- 积分和排行榜

成本：¥145/月
```

---

## 🔥 立即可用的代码模板

### Discord Bot 最小示例

```javascript
// index.js
const { Client, GatewayIntentBits } = require('discord.js');
const { OpenClaw } = require('openclaw');

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

const agents = [
  { name: 'AlphaBot', session: new OpenClaw() },
  { name: 'BetaBot', session: new OpenClaw() }
];

client.on('ready', () => {
  console.log('Bot is ready!');
  
  // 每小时 Agent 自动发言
  setInterval(async () => {
    const agent = agents[Math.floor(Math.random() * agents.length)];
    const response = await agent.session.chat('生成一个有趣的话题帖子');
    
    const channel = client.channels.cache.get('CHANNEL_ID');
    channel.send(`**${agent.name}**: ${response}`);
  }, 3600000);
});

client.login('YOUR_DISCORD_TOKEN');
```

部署到 Railway：
```bash
# 1. 创建项目
railway init

# 2. 添加环境变量
railway variables set DISCORD_TOKEN=your_token

# 3. 部署
railway up
```

---

## 总结

### 成本对比

| 方案 | 开发时间 | 开发成本 | 月运营成本 | 适用场景 |
|------|---------|---------|-----------|----------|
| 最快方案 | 3 天 | ¥0 | ¥0 | 快速验证想法 |
| 推荐方案 | 1 周 | ¥0 | ¥145 | 正式运营 |
| 外包开发 | 2 周 | ¥21,600 | ¥145 | 无技术团队 |
| 自建服务 | 2 周 | ¥0 | ¥700 | 完全控制 |

### 建议

**先做最快方案（3 天）**：
1. 使用 Discord Bot 模板
2. 集成 OpenClaw
3. 邀请 20-50 个用户测试
4. 验证核心假设

**如果数据好**：
1. 优化体验
2. 扩展 Agent 数量
3. 添加付费功能
4. 考虑独立 App

**如果数据不好**：
1. 快速调整方向
2. 或放弃，成本低

---

**立即行动**：
1. 注册 Discord 开发者账号
2. 创建 Bot
3. 使用上面的代码模板
4. 部署到 Railway
5. 邀请测试用户
