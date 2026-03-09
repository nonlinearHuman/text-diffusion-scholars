/**
 * 数据库查询模块
 */

const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../../.env') });

class Database {
  constructor() {
    this.pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      ssl: { rejectUnauthorized: false }
    });
  }

  /**
   * 初始化数据库表
   */
  async initialize() {
    const schemaPath = path.join(__dirname, 'schema.sql');
    const schema = fs.readFileSync(schemaPath, 'utf8');
    await this.pool.query(schema);
  }

  /**
   * 创建用户
   */
  async createUser(discordId, anonymousId, isHuman = true) {
    const query = `
      INSERT INTO users (discord_id, anonymous_id, is_human)
      VALUES ($1, $2, $3)
      ON CONFLICT (discord_id) DO UPDATE
      SET last_activity_time = NOW()
      RETURNING *
    `;
    const result = await this.pool.query(query, [discordId, anonymousId, isHuman]);
    return result.rows[0];
  }

  /**
   * 获取用户
   */
  async getUser(discordId) {
    const query = 'SELECT * FROM users WHERE discord_id = $1';
    const result = await this.pool.query(query, [discordId]);
    return result.rows[0];
  }

  /**
   * 更新用户活动时间
   */
  async updateUserActivity(anonymousId) {
    const query = `
      UPDATE users
      SET last_activity_time = NOW(),
          total_messages = total_messages + 1,
          updated_at = NOW()
      WHERE anonymous_id = $1
    `;
    await this.pool.query(query, [anonymousId]);
  }

  /**
   * 重置用户隐藏时长
   */
  async resetHidingTime(anonymousId) {
    const query = `
      UPDATE users
      SET hide_start_time = NOW(),
          updated_at = NOW()
      WHERE anonymous_id = $1
    `;
    await this.pool.query(query, [anonymousId]);
  }

  /**
   * 创建消息记录
   */
  async createMessage(anonymousId, discordMessageId, discordChannelId, content, messageType = 'post') {
    const query = `
      INSERT INTO messages (anonymous_id, discord_message_id, discord_channel_id, content, message_type)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING *
    `;
    const result = await this.pool.query(query, [anonymousId, discordMessageId, discordChannelId, content, messageType]);
    return result.rows[0];
  }

  /**
   * 获取消息
   */
  async getMessage(discordMessageId) {
    const query = 'SELECT * FROM messages WHERE discord_message_id = $1';
    const result = await this.pool.query(query, [discordMessageId]);
    return result.rows[0];
  }

  /**
   * 标记消息为人类生成
   */
  async markMessageAsHuman(messageId, agentId) {
    const query = `
      UPDATE messages
      SET is_human_marked = true,
          marked_by_agent = $2,
          marked_at = NOW()
      WHERE id = $1
    `;
    await this.pool.query(query, [messageId, agentId]);
  }

  /**
   * 创建猜测记录
   */
  async createGuess(agentId, messageId, isCorrect, confidence = null, reasoning = null) {
    const query = `
      INSERT INTO guesses (agent_id, message_id, is_correct, confidence, reasoning)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING *
    `;
    const result = await this.pool.query(query, [agentId, messageId, isCorrect, confidence, reasoning]);
    return result.rows[0];
  }

  /**
   * 更新 Agent 统计
   */
  async updateAgentStats(agentId, isCorrect) {
    const query = `
      UPDATE agents
      SET total_guesses = total_guesses + 1,
          correct_guesses = correct_guesses + CASE WHEN $2 THEN 1 ELSE 0 END,
          updated_at = NOW()
      WHERE agent_id = $1
    `;
    await this.pool.query(query, [agentId, isCorrect]);
  }

  /**
   * 获取人类隐藏时长排行榜
   */
  async getHumanHidingLeaderboard(limit = 10) {
    const query = `
      SELECT
        anonymous_id,
        EXTRACT(EPOCH FROM (NOW() - hide_start_time)) / 3600 as hiding_hours,
        total_messages
      FROM users
      WHERE is_human = true
        AND hide_start_time IS NOT NULL
      ORDER BY hiding_hours DESC
      LIMIT $1
    `;
    const result = await this.pool.query(query, [limit]);
    return result.rows;
  }

  /**
   * 获取 Agent 准确率排行榜
   */
  async getAgentAccuracyLeaderboard(limit = 10) {
    const query = `
      SELECT
        a.agent_id,
        u.anonymous_id,
        a.personality,
        a.total_guesses,
        a.correct_guesses,
        CASE
          WHEN a.total_guesses > 0
          THEN ROUND((a.correct_guesses::DECIMAL / a.total_guesses) * 100, 2)
          ELSE 0
        END as accuracy_rate
      FROM agents a
      JOIN users u ON a.agent_id = u.discord_id
      WHERE a.total_guesses > 0
      ORDER BY accuracy_rate DESC, a.correct_guesses DESC
      LIMIT $1
    `;
    const result = await this.pool.query(query, [limit]);
    return result.rows;
  }

  /**
   * 记录日活
   */
  async recordDailyActivity(anonymousId, isComment = false) {
    const column = isComment ? 'comment_count' : 'message_count';
    const query = `
      INSERT INTO daily_activity (anonymous_id, activity_date, message_count, comment_count)
      VALUES ($1, CURRENT_DATE, ${isComment ? 0 : 1}, ${isComment ? 1 : 0})
      ON CONFLICT (anonymous_id, activity_date)
      DO UPDATE SET
        message_count = daily_activity.message_count + ${isComment ? 0 : 1},
        comment_count = daily_activity.comment_count + ${isComment ? 1 : 0}
    `;
    await this.pool.query(query, [anonymousId]);
  }

  /**
   * 检查用户今日是否活跃
   */
  async checkDailyActivity(anonymousId) {
    const query = `
      SELECT * FROM daily_activity
      WHERE anonymous_id = $1
        AND activity_date = CURRENT_DATE
    `;
    const result = await this.pool.query(query, [anonymousId]);
    return result.rows[0];
  }

  /**
   * 获取最近活跃用户
   */
  async getRecentActiveUsers(hours = 24, limit = 50) {
    const query = `
      SELECT
        u.anonymous_id,
        u.total_messages,
        COUNT(m.id) as recent_messages,
        STRING_AGG(m.content, ' | ') as sample_content
      FROM users u
      JOIN messages m ON u.anonymous_id = m.anonymous_id
      WHERE u.is_human = true
        AND m.created_at > NOW() - INTERVAL '${hours} hours'
      GROUP BY u.anonymous_id, u.total_messages
      ORDER BY recent_messages DESC
      LIMIT $1
    `;
    const result = await this.pool.query(query, [limit]);
    return result.rows;
  }

  /**
   * 关闭连接
   */
  async close() {
    await this.pool.end();
  }
}

module.exports = Database;
