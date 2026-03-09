/**
 * Discord 事件处理模块
 */

const crypto = require('crypto');

/**
 * 生成匿名ID
 */
function generateAnonymousId(isHuman = true) {
  const prefix = isHuman ? 'human_' : 'agent_';
  const hash = crypto.randomBytes(4).toString('hex');
  return `${prefix}${hash}`;
}

/**
 * 处理消息事件
 */
async function handleMessage(message, agentManager, db) {
  // 忽略 Bot 消息
  if (message.author.bot) return;
  
  // 忽略私聊
  if (!message.guild) return;
  
  try {
    // 获取或创建用户
    let user = await db.getUser(message.author.id);
    
    if (!user) {
      // 检查是否是已注册的 Agent
      const isAgent = agentManager.isRegisteredAgent(message.author.id);
      const anonymousId = generateAnonymousId(!isAgent);
      
      user = await db.createUser(
        message.author.id, 
        anonymousId, 
        !isAgent
      );
      
      console.log(`✨ 新用户加入: ${anonymousId} (${isAgent ? 'Agent' : 'Human'})`);
    }
    
    // 更新用户活动
    await db.updateUserActivity(user.anonymous_id);
    
    // 记录消息
    await db.createMessage(
      user.anonymous_id,
      message.id,
      message.channel.id,
      message.content,
      'post'
    );
    
    // 记录日活
    await db.recordDailyActivity(user.anonymous_id);
    
    // 如果是人类，重置隐藏时长
    if (user.is_human) {
      // 不重置，保持隐藏时长累积
    }
    
    console.log(`📝 [${user.anonymous_id}]: ${message.content.substring(0, 50)}...`);
    
    // 回复用户
    await message.reply({
      content: `🎭 你好！你的匿名身份是：**${user.anonymous_id}**\n` +
               `已记录你的消息。发送 \`/help\` 查看命令。`
    });
    
  } catch (error) {
    console.error('❌ 消息处理失败:', error);
  }
}

module.exports = {
  handleMessage,
  generateAnonymousId
};
