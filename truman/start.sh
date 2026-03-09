#!/bin/bash
cd ~/.openclaw/workspace/truman

# 设置代理环境变量
export HTTPS_PROXY=http://127.0.0.1:7897
export HTTP_PROXY=http://127.0.0.1:7897
export ALL_PROXY=http://127.0.0.1:7897

# 启动 Bot
node src/bot/index.js
