#!/bin/bash
# Docker Desktop 下载脚本

echo "================================"
echo "Docker Desktop 下载"
echo "================================"
echo ""

# 切换到下载目录
cd ~/Downloads

echo "📥 开始下载 Docker Desktop..."
echo ""
echo "文件大小：约 620MB"
echo "下载位置：~/Downloads/Docker.dmg"
echo ""
echo "⏱️  预计时间：5-10 分钟（取决于网络速度）"
echo ""

# 下载
curl -L -O https://desktop.docker.com/mac/main/arm64/Docker.dmg

if [ -f "Docker.dmg" ]; then
    echo ""
    echo "✅ 下载完成！"
    echo ""
    echo "文件位置：~/Downloads/Docker.dmg"
    echo ""
    echo "================================"
    echo "安装步骤："
    echo ""
    echo "1. 双击打开 Docker.dmg"
    echo "2. 将 Docker 拖到 Applications"
    echo "3. 打开 Docker Desktop 应用"
    echo "4. 等待启动完成"
    echo ""
    echo "安装完成后回复：Docker 已安装"
    echo "================================"
else
    echo ""
    echo "❌ 下载失败"
    echo ""
    echo "请尝试："
    echo "1. 直接访问官网：https://www.docker.com/products/docker-desktop"
    echo "2. 或改用 Vercel 云部署"
fi
