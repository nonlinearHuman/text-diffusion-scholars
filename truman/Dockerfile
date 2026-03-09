FROM node:20-slim

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci --only=production

# 复制代码
COPY . .

# 启动
CMD ["node", "src/bot/index.js"]
