#!/bin/bash
# RSSHub Railway 一键部署

echo "================================"
echo "RSSHub 已准备就绪"
echo "================================"
echo ""
echo "📦 仓库地址："
echo "https://github.com/nonlinearHuman/rsshub"
echo ""
echo "================================"
echo ""
echo "🚀 部署到 Railway（2分钟）"
echo ""
echo "方式一：Railway 网站（推荐）"
echo ""
echo "1. 打开 Railway：https://railway.app"
echo ""
echo "2. 点击 'Start a New Project'"
echo ""
echo "3. 选择 'Deploy from GitHub repo'"
echo ""
echo "4. 选择 'nonlinearHuman/rsshub'"
echo ""
echo "5. 等待部署完成（约2分钟）"
echo ""
echo "6. 获取域名："
echo "   Settings → Domains → Generate Domain"
echo ""
echo "================================"
echo ""
echo "方式二：Railway CLI（更快）"
echo ""

# 检查是否安装 Railway CLI
if command -v railway &> /dev/null; then
    echo "✅ Railway CLI 已安装"
    echo ""
    railway login
    railway init
    railway up
else
    echo "安装 Railway CLI："
    echo "  npm i -g @railway/cli"
    echo ""
    echo "然后运行："
    echo "  railway login"
    echo "  railway init"
    echo "  railway up"
fi

echo ""
echo "================================"
