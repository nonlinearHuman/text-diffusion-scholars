# RSSHub 快速部署（3分钟完成）

## 🎯 方式一：Railway 一键部署（推荐）

### 第一步：Fork RSSHub（30秒）

1. 点击这个链接：https://github.com/DIYgod/RSSHub/fork
2. 点击右上角 **"Fork"** 按钮
3. 等待完成（约10秒）

### 第二步：部署到 Railway（2分钟）

1. **打开 Railway**：https://railway.app
2. **点击**："Start a New Project"
3. **选择**："Login with GitHub"
4. **授权**：允许 Railway 访问你的 GitHub
5. **点击**："+ New Project"
6. **选择**："Deploy from GitHub repo"
7. **选择**：你刚才 Fork 的 `RSSHub` 仓库
8. **等待**：2-3 分钟，状态变为 "SUCCESS"

### 第三步：获取域名（30秒）

1. 在 Railway 项目页面，点击 **"Settings"**
2. 点击 **"Domains"**
3. 点击 **"Generate Domain"**
4. 复制生成的域名（例如：`https://rsshub-production-abc.up.railway.app`）

### 第四步：测试

```bash
# 替换你的域名
curl https://你的域名/xueqiu/user/1247297532
```

---

## 🎯 方式二：Vercel 一键部署（更快）

### 第一步：Fork RSSHub
同上

### 第二步：部署到 Vercel（1分钟）

1. **打开 Vercel**：https://vercel.com
2. **点击**："Sign Up" → 选择 GitHub
3. **导入项目**：点击 "Import Project"
4. **选择仓库**：选择你 Fork 的 RSSHub
5. **点击 Deploy**：等待 1-2 分钟
6. **获取域名**：Vercel 自动分配（如：`https://rsshub.vercel.app`）

---

## 📝 部署完成后

告诉我你的域名，我帮你：
1. 更新脚本配置
2. 测试雪球路由
3. 安装定时任务

---

## ⚡ 快速检查清单

- [ ] GitHub 账号（没有就注册）
- [ ] Fork RSSHub 仓库
- [ ] 部署到 Railway 或 Vercel
- [ ] 获取域名
- [ ] 测试成功

---

**预计总时间：3-5 分钟**

**完成后把域名发给我，格式：**
```
我的域名：https://xxx.railway.app
```

或者：
```
我的域名：https://xxx.vercel.app
```
