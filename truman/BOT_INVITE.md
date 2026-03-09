# Trueman Bot 邀请链接

## 🎯 正确的邀请链接（包含 applications.commands）

```
https://discord.com/api/oauth2/authorize?client_id=1479114434612957428&permissions=2147483648&scope=bot%20applications.commands
```

## 📋 权限说明

- **permissions=2147483648** = 只包含 `USE_SLASH_COMMANDS` 权限
- **scope=bot%20applications.commands** = 包含 bot 和斜杠命令权限

---

## 🔧 操作步骤

### 步骤1：踢掉旧 Bot

1. 在 Discord 服务器中
2. 右键点击 **Trueman** Bot
3. 选择 **踢出 Trueman**

### 步骤2：用新链接邀请

1. 复制上面的链接
2. 在浏览器中打开
3. 选择你的服务器
4. 点击 **授权**
5. 完成人机验证

### 步骤3：验证权限

邀请完成后，检查：
- Bot 是否在服务器成员列表中
- Bot 角色是否有 "使用斜杠命令" 权限

---

## 🚀 启动 Bot

```bash
cd /Users/gesong/.openclaw/workspace/truman && bash start.sh
```

成功标志：
```
✅ 命令已注册到服务器: 1385660745861042319
```

---

## ⚠️ 如果还是不行

可能的原因：
1. **服务器权限不足** - 你需要服务器管理员权限
2. **Discord 缓存** - 等待 5-10 分钟再试
3. **链接错误** - 确认链接完整复制

---

*生成时间：2026-03-06*
