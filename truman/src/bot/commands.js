/**
 * Discord 命令处理模块
 */

const { SlashCommandBuilder, REST, Routes } = require('discord.js');

// 定义命令
const commands = [
  new SlashCommandBuilder()
    .setName('status')
    .setDescription('查看你的统计信息'),
  
  new SlashCommandBuilder()
    .setName('leaderboard')
    .setDescription('查看排行榜')
    .addStringOption(option =>
      option.setName('type')
        .setDescription('排行榜类型')
        .setRequired(true)
        .addChoices(
          { name: '人类隐藏时长', value: 'hiding' },
          { name: 'AI准确率', value: 'accuracy' }
        )),
  
  new SlashCommandBuilder()
    .setName('guess')
    .setDescription('猜测某条消息是否来自人类')
    .addStringOption(option =>
      option.setName('message_id')
        .setDescription('消息ID')
        .setRequired(true))
    .addBooleanOption(option =>
      option.setName('is_human')
        .setDescription('是否人类')
        .setRequired(true)),
  
  new SlashCommandBuilder()
    .setName('reveal')
    .setDescription('揭示你的真实身份（结束游戏）'),
  
  new SlashCommandBuilder()
    .setName('help')
    .setDescription('查看帮助信息'),
];

/**
 * 注册命令到 Discord
 */
async function setupCommands(client) {
  const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);
  
  try {
    console.log('📡 正在注册命令...');
    
    // 注册到特定服务器（开发环境）
    if (process.env.DISCORD_GUILD_ID) {
      await rest.put(
        Routes.applicationGuildCommands(process.env.DISCORD_CLIENT_ID, process.env.DISCORD_GUILD_ID),
        { body: commands.map(cmd => cmd.toJSON()) }
      );
      console.log(`✅ 命令已注册到服务器: ${process.env.DISCORD_GUILD_ID}`);
    } else {
      // 注册为全局命令（生产环境）
      await rest.put(
        Routes.applicationCommands(process.env.DISCORD_CLIENT_ID),
        { body: commands.map(cmd => cmd.toJSON()) }
      );
      console.log('✅ 全局命令已注册');
    }
  } catch (error) {
    console.error('❌ 注册命令失败:', error);
  }
}

/**
 * 处理斜杠命令
 */
async function handleCommand(interaction, agentManager, db) {
  if (!interaction.isChatInputCommand()) return;
  
  const { commandName } = interaction;
  
  try {
    switch (commandName) {
      case 'status': {
        const user = await db.getUser(interaction.user.id);
        if (!user) {
          await interaction.reply('你还没有开始游戏，发一条消息开始吧！');
          return;
        }
        
        const hidingHours = user.hide_start_time 
          ? ((Date.now() - new Date(user.hide_start_time).getTime()) / 3600000).toFixed(2)
          : 0;
        
        await interaction.reply({
          embeds: [{
            title: '📊 你的状态',
            fields: [
              { name: '匿名ID', value: user.anonymous_id, inline: true },
              { name: '身份', value: user.is_human ? '人类' : 'AI Agent', inline: true },
              { name: '隐藏时长', value: `${hidingHours} 小时`, inline: true },
              { name: '总消息数', value: String(user.total_messages), inline: true },
            ],
            color: user.is_human ? 0x00ff00 : 0xff6600,
          }],
          ephemeral: true
        });
        break;
      }
      
      case 'leaderboard': {
        const type = interaction.options.getString('type');
        
        if (type === 'hiding') {
          const data = await db.getHumanHidingLeaderboard(10);
          const lines = data.map((row, i) => 
            `${i + 1}. ${row.anonymous_id} - ${parseFloat(row.hiding_hours).toFixed(2)}小时 (${row.total_messages}条消息)`
          );
          
          await interaction.reply({
            embeds: [{
              title: '🏆 人类隐藏时长排行榜',
              description: lines.join('\n') || '暂无数据',
              color: 0x00ff00,
            }]
          });
        } else if (type === 'accuracy') {
          const data = await db.getAgentAccuracyLeaderboard(10);
          const lines = data.map((row, i) => 
            `${i + 1}. ${row.anonymous_id} - ${row.accuracy_rate}% (${row.correct_guesses}/${row.total_guesses})`
          );
          
          await interaction.reply({
            embeds: [{
              title: '🏆 AI准确率排行榜',
              description: lines.join('\n') || '暂无数据',
              color: 0xff6600,
            }]
          });
        }
        break;
      }
      
      case 'guess': {
        // 检查是否是人类尝试猜测
        const user = await db.getUser(interaction.user.id);
        if (user && user.is_human) {
          await interaction.reply({
            content: '人类不能参与猜测游戏，只有AI Agent才能猜测！',
            ephemeral: true
          });
          return;
        }
        
        const messageId = interaction.options.getString('message_id');
        const isHuman = interaction.options.getBoolean('is_human');
        
        const message = await db.getMessage(messageId);
        if (!message) {
          await interaction.reply({
            content: '找不到这条消息',
            ephemeral: true
          });
          return;
        }
        
        // 记录猜测
        const correct = message.anonymous_id.startsWith('human_') === isHuman;
        await db.createGuess(interaction.user.id, message.id, correct);
        await db.updateAgentStats(interaction.user.id, correct);
        
        await interaction.reply({
          content: correct 
            ? '✅ 猜对了！这条消息确实来自' + (isHuman ? '人类' : 'AI')
            : '❌ 猜错了！',
          ephemeral: true
        });
        break;
      }
      
      case 'reveal': {
        const user = await db.getUser(interaction.user.id);
        if (!user) {
          await interaction.reply('你还没有开始游戏！');
          return;
        }
        
        if (!user.is_human) {
          await interaction.reply('AI Agent 不能揭示身份！');
          return;
        }
        
        await interaction.reply({
          content: `🎭 你的真实身份是：**${interaction.user.username}**\n游戏结束，感谢参与！`,
          ephemeral: true
        });
        break;
      }
      
      case 'help': {
        await interaction.reply({
          embeds: [{
            title: '📖 楚门游戏帮助',
            description: '这是一个人类与AI Agent混合的社交实验。你的目标是隐藏自己的人类身份，让AI无法识别你。',
            fields: [
              { name: '/status', value: '查看你的统计信息' },
              { name: '/leaderboard', value: '查看排行榜' },
              { name: '/reveal', value: '揭示真实身份（结束游戏）' },
              { name: '/help', value: '显示此帮助信息' },
              { name: '\u200B', value: '\u200B' },
              { name: '游戏规则', value: '1. 发言时你的身份会被隐藏\n2. 隐藏时间越长，排名越高\n3. AI Agent会尝试猜测你是人类\n4. 一旦被识别，游戏结束' },
            ],
            color: 0x5865F2,
          }],
          ephemeral: true
        });
        break;
      }
    }
  } catch (error) {
    console.error('❌ 命令处理失败:', error);
    await interaction.reply({
      content: '处理命令时出错了',
      ephemeral: true
    });
  }
}

module.exports = {
  setupCommands,
  handleCommand,
  commands
};
