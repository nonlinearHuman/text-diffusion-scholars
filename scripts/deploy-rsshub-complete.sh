#!/bin/bash
# RSSHub 完整部署脚本（包含 Docker 启动检测）

echo "================================"
echo "RSSHub 完整部署"
echo "================================"
echo ""

# 等待 Docker 启动
echo "⏳ 等待 Docker Desktop 启动..."
echo ""

MAX_WAIT=60  # 最多等待60秒
WAIT_COUNT=0

while ! docker info &> /dev/null; do
    WAIT_COUNT=$((WAIT_COUNT + 1))
    
    if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
        echo ""
        echo "❌ Docker 启动超时"
        echo ""
        echo "请手动打开 Docker Desktop 应用，然后重新运行此脚本"
        exit 1
    fi
    
    echo -n "."
    sleep 2
done

echo ""
echo "✅ Docker 已就绪"
echo ""

# 检查并停止旧容器
echo "🔍 检查已有容器..."
docker stop rsshub 2>/dev/null && echo "  已停止旧容器"
docker rm rsshub 2>/dev/null && echo "  已删除旧容器"
echo ""

# 拉取并启动 RSSHub
echo "🚀 启动 RSSHub 容器..."
echo ""
echo "📥 拉取镜像（首次需要几分钟）..."
echo ""

docker run -d \
  --name rsshub \
  --restart unless-stopped \
  -p 1200:1200 \
  diygod/rsshub

if [ $? -eq 0 ]; then
    echo ""
    echo "⏳ 等待服务启动..."
    sleep 10
    
    echo ""
    echo "🧪 测试服务..."
    echo ""
    
    # 测试主服务
    if curl -s http://localhost:1200 > /dev/null 2>&1; then
        echo "✅ RSSHub 启动成功！"
        echo ""
        echo "================================"
        echo "访问地址："
        echo "  http://localhost:1200"
        echo ""
        echo "雪球路由："
        echo "  http://localhost:1200/xueqiu/user/1247297532"
        echo ""
        echo "================================"
        echo ""
        echo "管理命令："
        echo "  查看日志: docker logs rsshub"
        echo "  停止服务: docker stop rsshub"
        echo "  重启服务: docker restart rsshub"
        echo ""
        echo "================================"
        echo ""
        echo "✅ 部署完成！"
        echo ""
        echo "下一步：更新雪球脚本配置"
    else
        echo ""
        echo "⚠️  服务启动中，请稍后..."
        echo ""
        echo "查看日志："
        echo "  docker logs rsshub"
    fi
else
    echo ""
    echo "❌ 启动失败"
    echo ""
    echo "查看错误："
    echo "  docker logs rsshub"
fi
