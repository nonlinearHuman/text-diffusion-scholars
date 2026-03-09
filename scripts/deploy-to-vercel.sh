#!/bin/bash
# RSSHub Vercel 一键部署（更快）

echo "================================"
echo "RSSHub Vercel 一键部署"
echo "================================"
echo ""
echo "📦 仓库地址："
echo "https://github.com/nonlinearHuman/rsshub"
echo ""
echo "================================"
echo ""
echo "🚀 部署到 Vercel（1分钟）"
echo ""

# 检查是否安装 Vercel CLI
if command -v vercel &> /dev/null; then
    echo "✅ Vercel CLI 已安装"
    echo ""
    echo "部署步骤："
    echo "  cd /tmp"
    echo "  gh repo clone nonlinearHuman/rsshub"
    echo "  cd rsshub"
    echo "  vercel"
    echo ""
else
    echo "安装 Vercel CLI："
    echo "  npm i -g vercel"
    echo ""
    echo "然后运行："
    echo "  cd /tmp && gh repo clone nonlinearHuman/rsshub && cd rsshub && vercel"
fi

echo "================================"
