#!/bin/bash
# RSSHub Docker 一键部署脚本

echo "================================"
echo "RSSHub Docker 部署"
echo "================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    echo ""
    echo "请先安装 Docker Desktop："
    echo "  brew install --cask docker"
    echo ""
    echo "或访问：https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker 未运行"
    echo ""
    echo "请打开 Docker Desktop 应用"
    exit 1
fi

echo "✅ Docker 已就绪"
echo ""

# 停止并删除旧容器（如果存在）
echo "🔍 检查已有容器..."
docker stop rsshub 2>/dev/null
docker rm rsshub 2>/dev/null

echo ""
echo "🚀 启动 RSSHub 容器..."
echo ""

# 启动 RSSHub
docker run -d \
  --name rsshub \
  --restart unless-stopped \
  -p 1200:1200 \
  diygod/rsshub

# 等待启动
echo "⏳ 等待服务启动..."
sleep 5

# 测试
echo ""
echo "🧪 测试服务..."
if curl -s http://localhost:1200 > /dev/null; then
    echo ""
    echo "✅ RSSHub 启动成功！"
    echo ""
    echo "================================"
    echo "访问地址："
    echo "  http://localhost:1200"
    echo ""
    echo "雪球路由测试："
    echo "  http://localhost:1200/xueqiu/user/1247297532"
    echo ""
    echo "================================"
    echo ""
    echo "管理命令："
    echo "  查看日志: docker logs rsshub"
    echo "  停止服务: docker stop rsshub"
    echo "  重启服务: docker restart rsshub"
    echo "  删除容器: docker rm -f rsshub"
    echo ""
    echo "================================"
else
    echo ""
    echo "⚠️  服务启动中，请稍后重试"
    echo ""
    echo "查看日志："
    echo "  docker logs rsshub"
fi
