/**
 * 测试 Discord WebSocket 连接
 */

const WebSocket = require('ws');
const { HttpsProxyAgent } = require('https-proxy-agent');

const PROXY = process.env.HTTPS_PROXY || 'http://127.0.0.1:7897';
const DISCORD_GATEWAY = 'wss://gateway.discord.gg?v=10&encoding=json';

async function testConnection() {
  console.log('========================================');
  console.log('Discord WebSocket 连接测试');
  console.log('========================================');
  console.log(`📋 代理: ${PROXY}`);
  console.log(`📋 Gateway: ${DISCORD_GATEWAY}\n`);
  
  const agent = new HttpsProxyAgent(PROXY);
  const ws = new WebSocket(DISCORD_GATEWAY, { agent });
  
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      ws.terminate();
      reject(new Error('连接超时 (15秒)'));
    }, 15000);
    
    ws.on('open', () => {
      console.log('✅ WebSocket 连接成功！');
      clearTimeout(timeout);
      
      // 监听消息
      ws.on('message', (data) => {
        const msg = JSON.parse(data.toString());
        console.log(`📨 收到消息: op=${msg.op}`);
        
        if (msg.op === 10) { // Hello
          console.log(`   心跳间隔: ${msg.d?.heartbeat_interval}ms`);
          
          // 发送心跳
          ws.send(JSON.stringify({ op: 1, d: 1 }));
          console.log('   💓 发送心跳');
          
          // 发送 Identify
          const identify = {
            op: 2,
            d: {
              token: process.env.DISCORD_TOKEN,
              properties: {
                os: process.platform,
                browser: 'Truman Bot',
                device: 'Truman Bot'
              }
            }
          };
          ws.send(JSON.stringify(identify));
          console.log('   🔑 发送 Identify...');
        } else if (msg.op === 0) { // Dispatch
          console.log(`   事件: ${msg.t}`);
          if (msg.t === 'READY') {
            console.log('\n🎉 Discord 连接成功！');
            ws.close();
            resolve();
          }
        } else if (msg.op === 9) { // Invalid Session
          console.log(`   ❌ 会话无效: ${msg.d?.reason}`);
          ws.close();
          reject(new Error(msg.d?.reason));
        }
      });
    });
    
    ws.on('error', (err) => {
      clearTimeout(timeout);
      console.log(`❌ WebSocket 错误: ${err.message}`);
      reject(err);
    });
    
    ws.on('close', (code, reason) => {
      clearTimeout(timeout);
      console.log(`🔌 WebSocket 关闭: code=${code}, reason=${reason || '无'}`);
    });
  });
}

testConnection()
  .then(() => {
    console.log('\n✅ 测试通过！');
    process.exit(0);
  })
  .catch((err) => {
    console.log(`\n❌ 测试失败: ${err.message}`);
    process.exit(1);
  });
