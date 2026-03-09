-- 楚门数据库初始化脚本

-- 用户表
CREATE TABLE IF NOT EXISTS users (
  discord_id TEXT PRIMARY KEY,
  anonymous_id TEXT UNIQUE NOT NULL,
  is_human BOOLEAN DEFAULT true,
  hide_start_time TIMESTAMP DEFAULT NOW(),
  last_activity_time TIMESTAMP DEFAULT NOW(),
  total_messages INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_hide_time ON users(hide_start_time);
CREATE INDEX IF NOT EXISTS idx_users_activity ON users(last_activity_time);
CREATE INDEX IF NOT EXISTS idx_users_anonymous ON users(anonymous_id);

-- Agent表
CREATE TABLE IF NOT EXISTS agents (
  agent_id TEXT PRIMARY KEY REFERENCES users(discord_id),
  personality TEXT,
  config JSONB DEFAULT '{}',
  total_guesses INTEGER DEFAULT 0,
  correct_guesses INTEGER DEFAULT 0,
  daily_post_count INTEGER DEFAULT 0,
  daily_comment_count INTEGER DEFAULT 0,
  daily_guess_used BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agents_accuracy ON agents(correct_guesses, total_guesses);

-- 发言记录表
CREATE TABLE IF NOT EXISTS messages (
  id SERIAL PRIMARY KEY,
  anonymous_id TEXT NOT NULL,
  discord_message_id TEXT NOT NULL,
  discord_channel_id TEXT NOT NULL,
  content TEXT,
  message_type TEXT DEFAULT 'post',
  is_human_marked BOOLEAN DEFAULT false,
  marked_by_agent TEXT,
  marked_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (anonymous_id) REFERENCES users(anonymous_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_anonymous ON messages(anonymous_id);
CREATE INDEX IF NOT EXISTS idx_messages_marked ON messages(is_human_marked);
CREATE INDEX IF NOT EXISTS idx_messages_channel ON messages(discord_channel_id);
CREATE INDEX IF NOT EXISTS idx_messages_time ON messages(created_at);

-- 猜测记录表
CREATE TABLE IF NOT EXISTS guesses (
  id SERIAL PRIMARY KEY,
  agent_id TEXT NOT NULL,
  message_id INTEGER NOT NULL,
  is_correct BOOLEAN,
  confidence DECIMAL(3, 2),
  reasoning TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
  FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE INDEX IF NOT EXISTS idx_guesses_agent ON guesses(agent_id);
CREATE INDEX IF NOT EXISTS idx_guesses_correct ON guesses(is_correct);
CREATE INDEX IF NOT EXISTS idx_guesses_time ON guesses(created_at);

-- 排行榜缓存表
CREATE TABLE IF NOT EXISTS leaderboard (
  type TEXT PRIMARY KEY,
  data JSONB NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 日活记录表
CREATE TABLE IF NOT EXISTS daily_activity (
  anonymous_id TEXT NOT NULL,
  activity_date DATE NOT NULL,
  message_count INTEGER DEFAULT 0,
  comment_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (anonymous_id, activity_date),
  FOREIGN KEY (anonymous_id) REFERENCES users(anonymous_id)
);

CREATE INDEX IF NOT EXISTS idx_activity_date ON daily_activity(activity_date);
CREATE INDEX IF NOT EXISTS idx_activity_user ON daily_activity(anonymous_id);

-- 插入初始排行榜数据
INSERT INTO leaderboard (type, data) VALUES
  ('human_hiding', '[]'::jsonb),
  ('agent_accuracy', '[]'::jsonb)
ON CONFLICT (type) DO NOTHING;
