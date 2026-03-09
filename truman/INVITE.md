# 楚门 Bot 邀请指南

## 🔑 权限问题解决

当前错误：`Missing Access` (50001)

原因：Bot没有被授予注册命令的权限。

---

## ✅ 解决方案

### 方法1：重新邀请Bot（推荐）

**步骤：**

1. **踢掉旧Bot**
   - 在Discord服务器里，右键点击 **Trueman**
   - 选择 **踢出**

2. **使用新链接邀请**
   ```
   https://discord.com/api/oauth2/authorize?client_id=1479114434612957428&permissions=355392&scope=bot%20applications.commands
   ```

3. **权限说明**
   这个链接包含：
   - ✅ 查看频道
   - ✅ 发送消息
   - ✅ 管理消息（可选）
   - ✅ 嵌入链接
   - ✅ 读取消息历史
   - ✅ 使用外部表情（可选）
   - ✅ 添加反应（可选）
   - ✅ **applications.commands** scope（关键！）

---

### 方法2：检查Intent设置

1. 访问 [Bot设置页面](https://discord.com/developers/applications/1479114434612957428/bot)

2. 滚动到 **Privileged Gateway Intents**

3. 启用：
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent**（可选）

4. 点击 **Save Changes**

---

## 🧪 验证

重新邀请后，启动Bot：

```bash
cd /Users/gesong/.openclaw/workspace/truman && bash start.sh
```

**成功标志：**
```
✅ 命令已注册到服务器: 1385660745861042319
```

---

## 📋 如果还是不行

可能的原因：
1. Bot已经在服务器里，需要先踢掉
2. 需要服务器管理员权限才能邀请
3. Discord API缓存问题（等5分钟再试）

---

*生成时间：2026-03-06*
