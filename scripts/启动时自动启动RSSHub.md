# macOS 启动时自动启动 RSSHub

## 方式一：launchd（推荐）

创建启动服务，开机自动运行。

### 步骤

1. 创建 plist 文件：

```bash
nano ~/Library/LaunchAgents/com.user.rsshub.plist
```

2. 粘贴以下内容：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.rsshub</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/docker</string>
        <string>start</string>
        <string>rsshub</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

3. 加载服务：

```bash
launchctl load ~/Library/LaunchAgents/com.user.rsshub.plist
```

---

## 方式二：Docker Desktop 设置（最简单）

Docker Desktop 会自动启动容器（如果设置了 `--restart unless-stopped`）

1. 打开 Docker Desktop
2. Settings → General
3. 勾选 "Start Docker Desktop when you log in"
4. RSSHub 容器会自动启动

---

## 方式三：登录项（macOS 13+）

1. 系统设置 → 通用 → 登录项
2. 添加 Docker Desktop
3. Docker 会自动启动容器

---

## 验证自动启动

重启 Mac 后运行：

```bash
docker ps | grep rsshub
```

应该看到 RSSHub 容器在运行。

---

## 注意事项

- Docker Desktop 需要先启动
- 容器设置 `--restart unless-stopped` 会自动重启
- 如果 Mac 休眠，容器会暂停

---

**推荐**：使用方式二（Docker Desktop 设置），最简单。
