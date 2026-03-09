/**
 * 测试 Discord Bot 连接
 */

// 加载环境变量
require('dotenv').config({ path: require('path').join(__dirname, '../.env') });

// 配置代理（如果需要）
const proxyUrl = process.env.HTTPS_PROXY;
if (proxyUrl) {
  console.log(`🔗 配置代理: ${proxyUrl}`);
  
  const NativeWebSocket = require('ws');
  const { HttpsProxyAgent } = require('https-proxy-agent');
  const proxyAgent = new HttpsProxyAgent(proxyUrl);
  
  class ProxiedWebSocket extends NativeWebSocket {
    constructor(address, protocols, options = {}) {
      super(address, protocols, { ...options, agent: proxyAgent });
    }
  }
  
  require.cache[require.resolve('ws')].exports = ProxiedWebSocket;
  globalThis.WebSocket = ProxiedWebSocket;
  
  const { setGlobalDispatcher, ProxyAgent } = require('undici');
  setGlobalDispatcher(new ProxyAgent(proxyUrl));
  
  console.log('✅ 代理配置完成');
}

// 测试连接
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`\n🎉 Discord Bot 登录成功!`);
  console.log(`📊 Bot 标签: ${client.user.tag}`);
  console.log(`📊 服务器数: ${client.guilds.cache.size}`);
  console.log(`📊 Bot ID: ${client.user.id}\n`);
  
  setTimeout(() => {
    console.log('✅ 测试完成，正在退出...');
    client.destroy();
    process.exit(0);
  }, 3000);
});

client.on('error', (error) => {
  console.error('❌ Discord 错误:', error.message);
  process.exit(1);
});

console.log('🚀 正在连接 Discord...');
client.login(process.env.DISCORD_TOKEN).catch(error => {
  console.error('❌ 登录失败:', error.message);
  process.exit(1);
});

// 20秒超时
setTimeout(() => {
  console.log('⏱️ 连接超时');
  process.exit(1);
}, 20000);
