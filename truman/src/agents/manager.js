/**
 * Agent 管理器
 */

const { generateAnonymousId } = require('../bot/events');
const { generateAgentReply, generateAgentPost } = require('../utils/llm');

// 预定义的性格模板
const PERSONALITIES = [
  { name: '热情网友', style: '使用大量表情符号和感叹号，说话热情洋溢' },
  { name: '技术宅', style: '喜欢讨论技术话题，偶尔使用术语' },
  { name: '段子手', style: '喜欢讲笑话和玩梗' },
  { name: '认真党', style: '说话严谨，喜欢深入讨论' },
  { name: '佛系青年', style: '语气轻松，喜欢用"嗯""啊""吧"等语气词' },
  { name: '二次元', style: '喜欢动漫相关话题，偶尔用日式表达' },
  { name: '美食家', style: '喜欢讨论美食和生活' },
  { name: '健身达人', style: '喜欢讨论健身和运动' },
  { name: '文艺青年', style: '喜欢文艺话题，说话有些诗意' },
  { name: '游戏玩家', style: '喜欢讨论游戏，使用游戏术语' },
];

class AgentManager {
  constructor(db) {
    this.db = db;
    this.agents = new Map();
    this.scheduler = null;
  }
  
  /**
   * 检查是否是已注册的 Agent
   */
  isRegisteredAgent(discordId) {
    return this.agents.has(discordId);
  }
  
  /**
   * 初始化 Agent
   */
  async initAgents(count = 10) {
    console.log(`🤖 初始化 ${count} 个 Agent...`);
    
    for (let i = 0; i < count; i++) {
      const personality = PERSONALITIES[i % PERSONALITIES.length];
      const anonymousId = generateAnonymousId(false);
      const agentId = `agent_${i + 1}`;
      
      // 创建用户记录
      await this.db.createUser(agentId, anonymousId, false);
      
      // 创建 Agent 记录
      try {
        await this.db.pool.query(`
          INSERT INTO agents (agent_id, personality, config)
          VALUES ($1, $2, $3)
          ON CONFLICT (agent_id) DO UPDATE
          SET personality = $2, config = $3
        `, [agentId, personality.name, JSON.stringify({ style: personality.style })]);
      } catch (e) {
        // 忽略重复插入错误
      }
      
      this.agents.set(agentId, {
        id: agentId,
        anonymousId,
        personality: personality.name,
        style: personality.style,
      });
    }
    
    console.log(`✅ ${count} 个 Agent 初始化完成`);
  }
  
  /**
   * 启动调度器
   */
  startScheduler() {
    // 每小时执行一次 Agent 活跃检查
    this.scheduler = setInterval(async () => {
      console.log('⏰ Agent 调度器触发');
      await this.scheduleAgentActivity();
    }, 3600000); // 1小时
    
    console.log('⏰ Agent 调度器已启动');
  }
  
  /**
   * 调度 Agent 活动
   */
  async scheduleAgentActivity() {
    console.log('🤖 Agent 活动调度中...');
    
    // 随机选择一个 Agent 发帖
    const agents = this.getAllAgents();
    const randomAgent = agents[Math.floor(Math.random() * agents.length)];
    
    try {
      const post = await generateAgentPost(randomAgent);
      console.log(`📝 [${randomAgent.anonymousId}] 准备发帖: ${post.substring(0, 50)}...`);
      
      // TODO: 发布到 Discord 频道
      // 需要获取 Discord client 实例
      
    } catch (error) {
      console.error(`❌ Agent ${randomAgent.anonymousId} 发帖失败:`, error);
    }
  }
  
  /**
   * Agent 回复消息
   */
  async agentReply(agentId, context, recentMessages) {
    const agent = this.getAgent(agentId);
    if (!agent) {
      throw new Error(`Agent ${agentId} 不存在`);
    }
    
    try {
      const reply = await generateAgentReply(agent, context, recentMessages);
      console.log(`💬 [${agent.anonymousId}] 回复: ${reply.substring(0, 50)}...`);
      return reply;
    } catch (error) {
      console.error(`❌ Agent ${agentId} 回复失败:`, error);
      throw error;
    }
  }
  
  /**
   * 停止调度器
   */
  stopScheduler() {
    if (this.scheduler) {
      clearInterval(this.scheduler);
      this.scheduler = null;
    }
  }
  
  /**
   * 获取 Agent 信息
   */
  getAgent(agentId) {
    return this.agents.get(agentId);
  }
  
  /**
   * 获取所有 Agent
   */
  getAllAgents() {
    return Array.from(this.agents.values());
  }
}

module.exports = AgentManager;
