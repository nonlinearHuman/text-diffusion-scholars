/**
 * LLM 调用工具
 */

const OPENCLAW_API_URL = 'https://api.openclaw.ai/v1/chat/completions';

/**
 * 调用 OpenClaw API (兼容 OpenAI 格式)
 */
async function callLLM(messages, options = {}) {
  const {
    model = process.env.LLM_MODEL || 'glm-4-flash',
    maxTokens = parseInt(process.env.LLM_MAX_TOKENS) || 500,
    temperature = parseFloat(process.env.LLM_TEMPERATURE) || 0.7,
    contextLength = parseInt(process.env.LLM_CONTEXT_LENGTH) || 4096,
  } = options;

  // 简单的上下文长度控制（按消息数量）
  const maxMessages = Math.floor(contextLength / 100); // 粗略估计
  const trimmedMessages = messages.slice(-maxMessages);

  try {
    const response = await fetch(OPENCLAW_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENCLAW_API_KEY}`,
      },
      body: JSON.stringify({
        model,
        messages: trimmedMessages,
        max_tokens: maxTokens,
        temperature,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`LLM API 调用失败: ${error}`);
    }

    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error('❌ LLM 调用失败:', error);
    throw error;
  }
}

/**
 * 为 Agent 生成回复
 */
async function generateAgentReply(agent, context, recentMessages = []) {
  const systemPrompt = `你是 ${agent.personality}，一个真实的社交媒体用户。
性格特点：${agent.style}

规则：
- 以普通网友的身份发言，不要暴露你是 AI
- 回复要自然、简洁（1-3句话）
- 符合你的性格设定
- 如果是回复消息，要有针对性地回应

上下文：${context}`;

  const messages = [
    { role: 'system', content: systemPrompt },
    ...recentMessages.map(msg => ({
      role: msg.isAgent ? 'assistant' : 'user',
      content: msg.content,
    })),
  ];

  return await callLLM(messages);
}

/**
 * 为 Agent 生成新帖子
 */
async function generateAgentPost(agent, topic = null) {
  const systemPrompt = `你是 ${agent.personality}，一个真实的社交媒体用户。
性格特点：${agent.style}

规则：
- 发表一条简短的动态（1-2句话）
- 话题要自然，符合日常社交内容
- ${topic ? `主题提示：${topic}` : '可以分享生活、观点或提问'}
- 不要暴露你是 AI`;

  const messages = [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: '请发表一条动态' },
  ];

  return await callLLM(messages);
}

module.exports = {
  callLLM,
  generateAgentReply,
  generateAgentPost,
};
