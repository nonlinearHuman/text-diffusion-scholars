/**
 * 预加载脚本 - 必须在所有模块之前运行
 * 用法: node -r ./preload.js src/bot/index.js
 */

const proxyUrl = process.env.HTTPS_PROXY || process.env.HTTP_PROXY || process.env.ALL_PROXY;

if (proxyUrl) {
  // 1. 创建代理 WebSocket
  const WebSocket = require('ws');
  const { HttpsProxyAgent } = require('https-proxy-agent');
  const agent = new HttpsProxyAgent(proxyUrl);
  
  const OriginalWebSocket = WebSocket;
  class ProxiedWebSocket extends OriginalWebSocket {
    constructor(address, protocols, options = {}) {
      console.log(`🔗 WS连接: ${address.substring(0, 50)}...`);
      super(address, protocols, { ...options, agent });
    }
  }
  
  // 2. 设置全局 WebSocket
  globalThis.WebSocket = ProxiedWebSocket;
  
  // 3. 关键：让 shouldUseGlobalFetchAndWebSocket 返回 true
  // 通过伪装成 Bun 环境
  process.versions.bun = 'proxy-hack';
  
  // 4. 设置 HTTP 代理
  const { setGlobalDispatcher, ProxyAgent } = require('undici');
  setGlobalDispatcher(new ProxyAgent(proxyUrl));
  
  console.log(`🔗 预加载完成: ${proxyUrl}`);
}
