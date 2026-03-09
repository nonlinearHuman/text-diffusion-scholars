/**
 * 楚门 - Discord Bot 入口文件
 * 
 * 人类与AI Agent混合社区
 */

'use strict';

// ====== 第一步：配置代理（必须在所有模块加载前）======
const proxyUrl = process.env.HTTPS_PROXY || process.env.HTTP_PROXY || 'http://127.0.0.1:7897';

console.log(`🔗 配置代理: ${proxyUrl}`);

// 1. 配置 undici 全局代理（HTTP 请求）
const { setGlobalDispatcher, ProxyAgent } = require('undici');
setGlobalDispatcher(new ProxyAgent(proxyUrl));

// 2. 配置 WebSocket 代理
const { HttpsProxyAgent } = require('https-proxy-agent');
const wsAgent = new HttpsProxyAgent(proxyUrl);

// 保存原始 WebSocket
const NativeWebSocket = require('ws');

// 创建代理 WebSocket 类
class ProxiedWebSocket extends NativeWebSocket {
  constructor(address, protocols, options = {}) {
    // 强制注入代理 agent
    super(address, protocols, { ...options, agent: wsAgent });
  }
}

// 替换模块缓存
require.cache[require.resolve('ws')].exports = ProxiedWebSocket;

console.log('✅ 代理配置完成');

// ====== 第二步：加载模块 ======
const { Client, GatewayIntentBits } = require('discord.js');
const { setupCommands, handleCommand } = require('./commands');
const { handleMessage } = require('./events');
const AgentManager = require('../agents/manager');
const Database = require('../db/queries');
require('dotenv').config();

// 初始化数据库
const db = new Database();

// 配置 Discord Client
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ],
});

// 初始化 Agent 管理器
const agentManager = new AgentManager(db);

// Bot 就绪
client.once('ready', async () => {
  console.log(`\n🎉 Bot 登录成功: ${client.user.tag}`);
  console.log(`📊 服务器数: ${client.guilds.cache.size}`);

  try {
    await db.initialize();
    console.log('✅ 数据库初始化完成');

    await agentManager.initAgents(10);
    console.log('✅ Agent 初始化完成');

    agentManager.startScheduler();
    console.log('✅ Agent 调度器启动');

    await setupCommands(client);
    console.log('✅ 命令注册完成');

    console.log('\n🚀 楚门 Bot 已就绪！');
    console.log('📋 前往 Discord 服务器测试: https://discord.com/channels/' + process.env.DISCORD_GUILD_ID);

  } catch (error) {
    console.error('❌ 初始化失败:', error);
    process.exit(1);
  }
});

// 监听消息
client.on('messageCreate', async (message) => {
  if (message.author.bot) return;

  try {
    await handleMessage(message, agentManager, db);
    if (message.content.startsWith('/')) {
      await handleCommand(message, agentManager, db);
    }
  } catch (error) {
    console.error('❌ 消息处理失败:', error);
  }
});

// 监听斜杠命令
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  try {
    await handleCommand(interaction, agentManager, db);
  } catch (error) {
    console.error('❌ 命令处理失败:', error);
  }
});

// 错误处理
client.on('error', (error) => console.error('❌ Client 错误:', error.message));
client.on('warn', (warn) => console.warn('⚠️ 警告:', warn));

// 启动
console.log('🚀 Bot 正在启动...');
console.log('📋 Bot ID:', process.env.DISCORD_CLIENT_ID);
console.log('📋 Guild ID:', process.env.DISCORD_GUILD_ID);

client.login(process.env.DISCORD_TOKEN)
  .then(() => console.log('✅ 登录请求已发送，等待 WebSocket 连接...'))
  .catch((error) => {
    console.error('❌ 登录失败:', error.message);
    process.exit(1);
  });

// 优雅关闭
const shutdown = async () => {
  console.log('\n📴 正在关闭...');
  agentManager.stopScheduler();
  await db.close();
  client.destroy();
  process.exit(0);
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

module.exports = client;
