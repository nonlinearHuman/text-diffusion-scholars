/**
 * 代理连接测试脚本
 */

const { HttpsProxyAgent } = require('https-proxy-agent');
const { setGlobalDispatcher, ProxyAgent } = require('undici');
const WebSocket = require('ws');
const https = require('https');

const PROXY = process.env.HTTPS_PROXY || 'http://127.0.0.1:7897';
const DISCORD_GATEWAY = 'wss://gateway.discord.gg?v=10&encoding=json';
const DISCORD_API = 'https://discord.com/api/v10/gateway';

async function testProxy() {
  console.log('========================================');
  console.log('楚门 Bot 代理连接测试');
  console.log('========================================\n');
  
  console.log(`📋 代理地址: ${PROXY}\n`);
  
  // 1. 测试 HTTP 代理
  console.log('1️⃣  测试 HTTP 代理...');
  try {
    setGlobalDispatcher(new ProxyAgent(PROXY));
    const res = await fetch(DISCORD_API);
    const data = await res.json();
    console.log(`   ✅ HTTP 代理正常`);
    console.log(`   📊 Gateway: ${data.url}\n`);
  } catch (e) {
    console.log(`   ❌ HTTP 代理失败: ${e.message}\n`);
    return false;
  }
  
  // 2. 测试 WebSocket 代理
  console.log('2️⃣  测试 WebSocket 代理...');
  try {
    const agent = new HttpsProxyAgent(PROXY);
    const ws = new WebSocket(DISCORD_GATEWAY, { agent });
    
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        ws.terminate();
        reject(new Error('连接超时 (10秒)'));
      }, 10000);
      
      ws.on('open', () => {
        clearTimeout(timeout);
        console.log('   ✅ WebSocket 代理正常\n');
        ws.close();
        resolve();
      });
      
      ws.on('error', (e) => {
        clearTimeout(timeout);
        reject(e);
      });
    });
  } catch (e) {
    console.log(`   ❌ WebSocket 代理失败: ${e.message}\n`);
    return false;
  }
  
  // 3. 测试 Discord.js 风格的连接
  console.log('3️⃣  测试 Discord.js WebSocket...');
  try {
    // Discord.js 使用 @discordjs/ws，它内部使用 ws 模块
    // 问题在于 Discord.js 如何创建 WebSocket 实例
    
    const agent = new HttpsProxyAgent(PROXY);
    
    // 模拟 Discord.js 的 WebSocket 创建方式
    const ws = new WebSocket(DISCORD_GATEWAY, {
      agent,
      handshakeTimeout: 30000,
      maxPayload: 104857600,
    });
    
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        ws.terminate();
        reject(new Error('Discord.js WebSocket 超时'));
      }, 15000);
      
      ws.on('open', () => {
        clearTimeout(timeout);
        console.log('   ✅ Discord.js 风格 WebSocket 正常');
        
        // 接收 Hello 消息
        ws.once('message', (data) => {
          const msg = JSON.parse(data.toString());
          console.log(`   📊 收到 Hello: heartbeat_interval=${msg.d?.heartbeat_interval}`);
          ws.close();
          resolve();
        });
      });
      
      ws.on('error', (e) => {
        clearTimeout(timeout);
        reject(e);
      });
    });
  } catch (e) {
    console.log(`   ❌ Discord.js WebSocket 失败: ${e.message}\n`);
    return false;
  }
  
  console.log('\n========================================');
  console.log('✅ 所有代理测试通过！');
  console.log('========================================\n');
  return true;
}

testProxy()
  .then(success => process.exit(success ? 0 : 1))
  .catch(e => {
    console.error('❌ 测试失败:', e);
    process.exit(1);
  });
