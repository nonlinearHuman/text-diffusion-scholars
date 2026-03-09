# RSSHub 自建部署指南（推荐方案）

## 🎯 为什么自建？

- ✅ **无需Cookie** - 公开数据，无需登录
- ✅ **永久稳定** - 不受公共实例限制
- ✅ **完全免费** - Docker 一键部署
- ✅ **隐私安全** - 数据在本地

---

## 📦 方式一：Docker 部署（推荐）

### 前提条件
- 已安装 Docker Desktop

### 部署步骤

```bash
# 1. 拉取镜像并启动
docker run -d \
  --name rsshub \
  -p 1200:1200 \
  --restart unless-stopped \
  diygod/rsshub

# 2. 验证部署
curl http://localhost:1200

# 3. 测试雪球路由
curl http://localhost:1200/xueqiu/user/1247297532
```

### 修改脚本

编辑 `xueqiu_rsshub.py`：

```python
CONFIG = {
    "rsshub_url": "http://localhost:1200/xueqiu/user/{user_id}",
    ...
}
```

---

## 📦 方式二：Railway 部署（云端）

### 优点
- 无需本地运行
- 公网可访问
- 免费额度足够

### 步骤

1. **Fork RSSHub 仓库**
   - 访问 https://github.com/DIYgod/RSSHub
   - 点击 Fork

2. **部署到 Railway**
   - 访问 https://railway.app
   - 用 GitHub 登录
   - 点击 "+ New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你 Fork 的 RSSHub 仓库
   - 等待部署完成（约 2-3 分钟）

3. **获取访问地址**
   - 在 Railway 项目页面
   - 点击 "Settings" → "Domains"
   - 添加自定义域名或使用默认域名
   - 例如：`https://your-app.railway.app`

4. **测试**
   ```bash
   curl https://your-app.railway.app/xueqiu/user/1247297532
   ```

---

## 📦 方式三：Vercel 部署（最快）

### 优点
- 全球 CDN
- 自动 HTTPS
- 免费额度大

### 步骤

1. **一键部署**
   - 访问 https://vercel.com
   - 导入 GitHub 仓库：`DIYgod/RSSHub`
   - 点击 Deploy

2. **等待完成**
   - 约 1-2 分钟

3. **获取地址**
   - Vercel 会分配域名：`https://rsshub.vercel.app`

---

## 🔧 修改配置

部署完成后，修改脚本：

```python
# 本地 Docker
CONFIG = {
    "rsshub_url": "http://localhost:1200/xueqiu/user/{user_id}",
    ...
}

# Railway/Vercel
CONFIG = {
    "rsshub_url": "https://your-domain.com/xueqiu/user/{user_id}",
    ...
}
```

---

## 🧪 测试

```bash
# 测试本地实例
/Users/gesong/.openclaw/workspace/scripts/xueqiu_rsshub.py

# 或测试云端实例
curl https://your-domain.com/xueqiu/user/1247297532 | head -20
```

---

## 📊 对比

| 方式 | 成本 | 稳定性 | 速度 | 推荐度 |
|------|------|--------|------|--------|
| Docker本地 | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Railway | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Vercel | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 💡 推荐

- **有Mac/服务器** → Docker本地部署
- **想云端运行** → Railway（推荐）或 Vercel

---

## 🆘 故障排查

### Docker 启动失败
```bash
# 查看日志
docker logs rsshub

# 重启容器
docker restart rsshub
```

### Railway 部署失败
- 检查 GitHub 仓库是否完整
- 查看 Railway 日志
- 尝试重新部署

### 访问超时
- 检查防火墙设置
- 尝试使用代理
- 更换部署平台

---

**需要帮助？告诉我你选择哪种方式，我帮你完成部署！**
