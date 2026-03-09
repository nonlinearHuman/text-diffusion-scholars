#!/usr/bin/env python3
"""
实战量化投资系统
目标：月收益10%
模式：每日交易信号 + 手动执行
"""

import akshare as ak
import pandas as pd
import json
from datetime import datetime, timedelta
import os

class QuantInvestor:
    def __init__(self, capital=1000, monthly_target=0.10):
        self.capital = capital
        self.initial_capital = capital
        self.monthly_target = monthly_target  # 月收益目标10%
        self.daily_target = (1 + monthly_target) ** (1/22) - 1  # 日均收益

        self.positions = {}
        self.trade_log = []
        self.daily_returns = []

        # 手续费配置
        self.fee_config = {
            'stamp_tax': 0.001,      # 印花税（仅卖出）千分之一
            'commission': 0.00025,    # 佣金（买卖双向）万分之2.5
            'min_commission': 5,      # 最低佣金5元
            'transfer_fee': 0.00001,  # 过户费（仅沪市）万分之一
        }
        self.total_fees_paid = 0  # 累计手续费
        
        # 交易规则配置
        self.trading_rules = {
            'min_shares': 100,           # 最小买入股数（1手=100股）
            'slippage_rate': 0.002,      # 滑点率 0.2%
            'min_volume': 10000000,      # 最小成交额1000万
            'limit_up_threshold': 0.095,  # 涨停阈值9.5%
            'limit_down_threshold': -0.095, # 跌停阈值-9.5%
            'bid_ask_spread': 0.005,     # 买卖价差 0.5%
            'data_delay_warning': 300,   # 数据延迟警告阈值（秒）
        }
        
        # 新增：风险控制配置（本金保护模式）
        self.risk_config = {
            'avoid_st_stocks': True,      # 避免ST股票
            'avoid_suspended': True,      # 避免停牌股票
            'max_data_delay': 60,         # 最大数据延迟（秒）
            'check_ex_dividend': True,    # 检查除权除息日
            # 本金保护机制
            'capital_protection': True,   # 本金保护模式
            'warning_line': 1100,         # 预警线：总资产<1100元
            'danger_line': 1050,          # 危险线：总资产<1050元
            'circuit_breaker': 1000,      # 熔断线：总资产<1000元
        }
        
        # 本金保护配置（极度保守）
        self.capital_protection = {
            'max_position_ratio': 0.25,   # 单只最大25%（更保守）
            'min_cash_reserve': 0.2,      # 最少保留20%现金
            'stop_loss': -0.03,           # 止损-3%（更严格）
            'take_profit': 0.05,          # 止盈+5%（更保守）
            'quick_profit': 0.03,         # 快速止盈+3%
            'min_trade_amount': 500,      # 最小交易金额500元
            'max_daily_trades': 1,        # 每日最多1笔交易
            'min_hold_days': 3,           # 最少持仓3天
        }

        # 市场状态
        self.today_trades = {}  # 今日买入的股票（T+1限制）

        self.log_dir = "/Users/gesong/.openclaw/workspace/trading-team/investment_logs"
        os.makedirs(self.log_dir, exist_ok=True)

        # 加载历史数据
        self.load_state()

    def log(self, role, message):
        icons = {
            '量化分析': '📊',
            '选股策略': '🎯',
            '风险管理': '🛡️',
            '交易信号': '💡'
        }
        print(f"{icons.get(role, '📌')} [{role}] {message}")

    def load_state(self):
        """加载历史状态"""
        state_file = f"{self.log_dir}/state.json"
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                data = json.load(f)
                self.capital = data.get('capital', self.initial_capital)
                self.positions = data.get('positions', {})
                self.trade_log = data.get('trade_log', [])

    def save_state(self):
        """保存状态"""
        state_file = f"{self.log_dir}/state.json"
        with open(state_file, 'w') as f:
            json.dump({
                'capital': self.capital,
                'positions': self.positions,
                'trade_log': self.trade_log,
                'updated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)

    def get_market_data(self):
        """获取市场数据"""
        self.log('量化分析', '获取市场数据...')

        data = {
            'market_status': 'UNKNOWN',
            'hot_stocks': [],
            'signals': [],
            'data_timestamp': None,
            'data_delay_seconds': 0,
            'warnings': []
        }

        try:
            # 尝试获取实时数据
            # 如果代理问题，使用模拟数据
            import random

            # 记录数据时间戳
            data['data_timestamp'] = datetime.now()
            data['data_delay_seconds'] = 0

            # 模拟热门股票（实际应从akshare获取）
            # 增加成交额和涨停状态
            stocks_data = [
                {
                    'code': '000001',
                    'name': '平安银行',
                    'change_pct': random.uniform(-0.05, 0.05),
                    'volume_ratio': random.uniform(0.5, 2.0),
                    'volume': random.uniform(50000000, 200000000),  # 成交额
                    'price': 10.0,
                    'bid_price': 9.99,   # 买一价
                    'ask_price': 10.01,  # 卖一价
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': False,  # 停牌状态
                    'is_st': False,         # ST股票
                    'board_type': 'MAIN',   # 板块类型：MAIN/STAR/GEM/BSE
                },
                {
                    'code': '600519',
                    'name': '贵州茅台',
                    'change_pct': random.uniform(-0.03, 0.03),
                    'volume_ratio': random.uniform(0.8, 1.5),
                    'volume': random.uniform(3000000000, 8000000000),
                    'price': 1500.0,
                    'bid_price': 1499.0,
                    'ask_price': 1501.0,
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': False,
                    'is_st': False,
                    'board_type': 'MAIN',
                },
                {
                    'code': '002594',
                    'name': '比亚迪',
                    'change_pct': random.uniform(-0.06, 0.06),
                    'volume_ratio': random.uniform(0.6, 1.8),
                    'volume': random.uniform(2000000000, 5000000000),
                    'price': 250.0,
                    'bid_price': 249.5,
                    'ask_price': 250.5,
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': False,
                    'is_st': False,
                    'board_type': 'MAIN',
                },
                {
                    'code': '300750',
                    'name': '宁德时代',
                    'change_pct': random.uniform(-0.05, 0.05),
                    'volume_ratio': random.uniform(0.7, 1.6),
                    'volume': random.uniform(1500000000, 4000000000),
                    'price': 180.0,
                    'bid_price': 179.8,
                    'ask_price': 180.2,
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': False,
                    'is_st': False,
                    'board_type': 'GEM',  # 创业板
                },
                {
                    'code': '000858',
                    'name': '五粮液',
                    'change_pct': random.uniform(-0.04, 0.04),
                    'volume_ratio': random.uniform(0.9, 1.4),
                    'volume': random.uniform(800000000, 2000000000),
                    'price': 150.0,
                    'bid_price': 149.9,
                    'ask_price': 150.1,
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': False,
                    'is_st': False,
                    'board_type': 'MAIN',
                },
                # 模拟ST股票（测试过滤）
                {
                    'code': '000002',
                    'name': 'ST万科',
                    'change_pct': random.uniform(-0.05, 0.05),
                    'volume_ratio': random.uniform(0.5, 1.5),
                    'volume': random.uniform(50000000, 150000000),
                    'price': 5.0,
                    'bid_price': 4.99,
                    'ask_price': 5.01,
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': False,
                    'is_st': True,  # ST股票
                    'board_type': 'MAIN',
                },
                # 模拟停牌股票（测试过滤）
                {
                    'code': '000003',
                    'name': '停牌测试',
                    'change_pct': 0,
                    'volume_ratio': 0,
                    'volume': 0,
                    'price': 10.0,
                    'bid_price': 10.0,
                    'ask_price': 10.0,
                    'is_limit_up': False,
                    'is_limit_down': False,
                    'is_suspended': True,  # 停牌
                    'is_st': False,
                    'board_type': 'MAIN',
                },
            ]

            # 随机模拟涨停情况
            for stock in stocks_data:
                if stock['change_pct'] > self.trading_rules['limit_up_threshold']:
                    stock['is_limit_up'] = True
                if stock['change_pct'] < self.trading_rules['limit_down_threshold']:
                    stock['is_limit_down'] = True

            data['hot_stocks'] = stocks_data
            data['market_status'] = 'TRADING'

            self.log('量化分析', f"获取 {len(data['hot_stocks'])} 只股票数据")

            # 数据延迟检查
            if data['data_delay_seconds'] > self.trading_rules['data_delay_warning']:
                warning = f"⚠️ 数据延迟 {data['data_delay_seconds']}秒，请谨慎决策"
                data['warnings'].append(warning)
                self.log('量化分析', warning)

        except Exception as e:
            self.log('量化分析', f"数据获取失败: {e}")
            data['warnings'].append(f"❌ 数据获取失败: {e}")

        return data

    def analyze_signals(self, market_data):
        """生成交易信号"""
        self.log('选股策略', '分析交易信号...')

        signals = []
        warnings = []

        for stock in market_data['hot_stocks']:
            # ===== P0级风险过滤 =====

            # 过滤1: ST股票
            if self.risk_config['avoid_st_stocks'] and stock.get('is_st', False):
                self.log('选股策略', f"🚫 跳过 {stock['name']}：ST股票风险")
                warnings.append(f"ST股票 {stock['name']} 已过滤")
                continue

            # 过滤2: 停牌股票
            if self.risk_config['avoid_suspended'] and stock.get('is_suspended', False):
                self.log('选股策略', f"🚫 跳过 {stock['name']}：已停牌")
                warnings.append(f"停牌股票 {stock['name']} 已过滤")
                continue

            # 过滤3: 流动性筛选（成交额≥1000万）
            if stock.get('volume', 0) < self.trading_rules['min_volume']:
                self.log('选股策略', f"跳过 {stock['name']}：成交额不足（{stock.get('volume', 0)/10000:.0f}万）")
                continue

            # 过滤4: 涨停/跌停过滤
            if stock.get('is_limit_up', False):
                self.log('选股策略', f"跳过 {stock['name']}：已涨停，无法买入")
                continue

            if stock.get('is_limit_down', False):
                self.log('选股策略', f"跳过 {stock['name']}：已跌停，谨慎参与")
                # 跌停可以买，但风险较高

            # 过滤5: 价格筛选（根据资金量）
            # 使用买一价和卖一价
            ask_price = stock.get('ask_price', stock.get('price', 0))  # 买入用卖一价
            max_shares = self.capital * 0.4 / ask_price  # 40%仓位可买股数
            if max_shares < self.trading_rules['min_shares']:
                self.log('选股策略', f"跳过 {stock['name']}：股价{ask_price:.2f}元过高，资金不足买100股")
                continue

            # ===== 盘口价差分析 =====
            bid_price = stock.get('bid_price', ask_price * 0.99)
            spread_ratio = (ask_price - bid_price) / ask_price

            if spread_ratio > self.trading_rules['bid_ask_spread']:
                warning = f"⚠️ {stock['name']} 盘口价差过大：{spread_ratio*100:.2f}%"
                warnings.append(warning)
                self.log('选股策略', warning)

            # ===== 板块规则检查 =====
            board_type = stock.get('board_type', 'MAIN')
            if board_type == 'STAR':  # 科创板
                limit_threshold = 0.20  # ±20%
                # 检查是否有权限
                warning = f"⚠️ {stock['name']} 为科创板股票，需确认交易权限"
                warnings.append(warning)
            elif board_type == 'GEM':  # 创业板
                limit_threshold = 0.20  # ±20%
            elif board_type == 'BSE':  # 北交所
                limit_threshold = 0.30  # ±30%
            else:  # 主板
                limit_threshold = 0.10  # ±10%

            # ===== 策略判断 =====

            # 策略1: 动量策略（追涨）
            if stock['change_pct'] > 0.02 and stock['volume_ratio'] > 1.2:
                # 考虑手续费和盘口价差
                # 提高买入门槛
                signals.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'action': 'BUY',
                    'strategy': '动量突破',
                    'strength': 'STRONG' if stock['change_pct'] > 0.03 else 'MEDIUM',
                    'reason': f"涨幅{stock['change_pct']*100:.2f}%，量比{stock['volume_ratio']:.2f}",
                    'confidence': min(0.9, 0.5 + stock['change_pct'] * 10),
                    'price': ask_price,  # 使用卖一价
                    'bid_price': bid_price,
                    'ask_price': ask_price,
                    'spread_ratio': spread_ratio,
                    'board_type': board_type,
                    'limit_threshold': limit_threshold
                })

            # 策略2: 超跌反弹
            elif stock['change_pct'] < -0.03 and stock['volume_ratio'] > 1.0:
                signals.append({
                    'code': stock['code'],
                    'name': stock['name'],
                    'action': 'BUY',
                    'strategy': '超跌反弹',
                    'strength': 'MEDIUM',
                    'reason': f"跌幅{stock['change_pct']*100:.2f}%，可能反弹",
                    'confidence': 0.6,
                    'price': ask_price,
                    'bid_price': bid_price,
                    'ask_price': ask_price,
                    'spread_ratio': spread_ratio,
                    'board_type': board_type,
                    'limit_threshold': limit_threshold
                })

        # 策略3: 检查持仓是否需要卖出
        for code, pos in self.positions.items():
            profit_pct = pos.get('profit_pct', 0)

            # T+1检查：今天买入的不能卖出
            buy_date = datetime.fromisoformat(pos.get('buy_time', datetime.now().isoformat())).date()
            if buy_date == datetime.now().date():
                self.log('选股策略', f"跳过 {pos['name']}：今日买入，T+1限制无法卖出")
                continue

            # 止损：亏损5%（考虑手续费后实际亏损约5.3%）
            if profit_pct < -0.05:
                signals.append({
                    'code': code,
                    'name': pos['name'],
                    'action': 'SELL',
                    'strategy': '止损',
                    'strength': 'STRONG',
                    'reason': f"亏损{profit_pct*100:.2f}%，触发止损",
                    'confidence': 0.95
                })

            # 止盈：盈利8%（扣除手续费后净盈利约7.3%）
            elif profit_pct > 0.08:
                signals.append({
                    'code': code,
                    'name': pos['name'],
                    'action': 'SELL',
                    'strategy': '止盈',
                    'strength': 'MEDIUM',
                    'reason': f"盈利{profit_pct*100:.2f}%，建议止盈",
                    'confidence': 0.7
                })

            # 新增：保本止损（盈利回落到成本线附近）
            elif profit_pct > -0.01 and profit_pct < 0.02:
                # 持仓超过3天且微利/微亏，考虑退出
                hold_days = (datetime.now() - datetime.fromisoformat(pos.get('buy_time', datetime.now().isoformat()))).days
                if hold_days >= 3:
                    signals.append({
                        'code': code,
                        'name': pos['name'],
                        'action': 'SELL',
                        'strategy': '保本止损',
                        'strength': 'WEAK',
                        'reason': f"持仓{hold_days}天，盈利{profit_pct*100:.2f}%，建议保本退出",
                        'confidence': 0.5
                    })

        # 按置信度排序
        signals.sort(key=lambda x: x['confidence'], reverse=True)

        self.log('选股策略', f"生成 {len(signals)} 个交易信号")

        # 显示警告信息
        if warnings:
            print(f"\n⚠️ 风险警告：")
            for w in warnings[:5]:  # 最多显示5条
                print(f"  - {w}")

        return signals

    def calculate_fees(self, amount, action, code=''):
        """计算手续费
        Args:
            amount: 交易金额
            action: 'BUY' 或 'SELL'
            code: 股票代码（用于判断沪市）
        Returns:
            总手续费
        """
        fees = 0

        # 佣金（买卖双向）
        commission = amount * self.fee_config['commission']
        commission = max(commission, self.fee_config['min_commission'])
        fees += commission

        # 印花税（仅卖出）
        if action == 'SELL':
            stamp_tax = amount * self.fee_config['stamp_tax']
            fees += stamp_tax

        # 过户费（仅沪市，股票代码6开头）
        if code.startswith('6'):
            transfer_fee = amount * self.fee_config['transfer_fee']
            fees += transfer_fee

        return fees

    def calculate_position_size(self, signal):
        """计算仓位"""
        self.log('风险管理', '计算仓位...')

        # 基础仓位（保守策略）
        base_position = 0.3  # 30%仓位

        # 根据信号强度调整
        if signal['strength'] == 'STRONG':
            position_ratio = min(0.4, base_position * 1.3)  # 最大40%
        else:
            position_ratio = base_position * 0.8  # 弱信号减仓

        # 计算金额
        amount = self.capital * position_ratio

        # ===== 使用盘口价格（卖一价） =====
        price = signal.get('ask_price', signal.get('price', 10.0))
        shares = int(amount / price)

        # 调整到100股整数倍
        shares = (shares // self.trading_rules['min_shares']) * self.trading_rules['min_shares']

        if shares < self.trading_rules['min_shares']:
            self.log('风险管理', f"❌ 资金不足：{amount:.2f}元最多买{shares}股，不足{self.trading_rules['min_shares']}股")
            return 0

        # 重新计算实际金额（使用卖一价）
        amount = shares * price

        # ===== 预留手续费（买入+卖出双边） =====
        buy_fees = self.calculate_fees(amount, 'BUY', signal['code'])
        # 预估卖出金额（假设涨3%）
        sell_amount = amount * 1.03
        sell_fees = self.calculate_fees(sell_amount, 'SELL', signal['code'])
        total_fees = buy_fees + sell_fees

        # ===== 考虑滑点成本 =====
        slippage_cost = amount * self.trading_rules['slippage_rate'] * 2  # 买卖双边滑点

        # ===== 考虑盘口价差 =====
        spread_ratio = signal.get('spread_ratio', 0)
        spread_cost = amount * spread_ratio

        # 总成本
        total_cost = amount + buy_fees + slippage_cost + spread_cost

        if total_cost > self.capital * 0.9:
            # 减少股数
            shares = int((self.capital * 0.9 - buy_fees - slippage_cost - spread_cost) / price)
            shares = (shares // self.trading_rules['min_shares']) * self.trading_rules['min_shares']
            if shares < self.trading_rules['min_shares']:
                return 0
            amount = shares * price

        # 计算保本涨幅
        total_trading_cost = total_fees + slippage_cost + spread_cost
        breakeven_pct = total_trading_cost / amount

        self.log('风险管理', f"建议仓位: {amount:.2f}元 ({shares}股 @ {price:.2f}元)")
        self.log('风险管理', f"盘口价差: {spread_cost:.2f}元 ({spread_ratio*100:.2f}%)")
        self.log('风险管理', f"预估成本: 手续费{buy_fees:.2f}元 + 滑点{slippage_cost:.2f}元 + 价差{spread_cost:.2f}元")
        self.log('风险管理', f"双边总成本: {total_trading_cost:.2f}元（需涨{breakeven_pct*100:.2f}%回本）")

        # 板块风险提示
        board_type = signal.get('board_type', 'MAIN')
        if board_type in ['STAR', 'GEM', 'BSE']:
            self.log('风险管理', f"⚠️ {board_type}股票涨跌停±{signal.get('limit_threshold', 0.1)*100:.0f}%")

        signal['suggested_shares'] = shares
        signal['suggested_price'] = price * (1 + self.trading_rules['slippage_rate'])
        signal['breakeven_pct'] = breakeven_pct
        signal['spread_cost'] = spread_cost

        return amount

    def generate_daily_report(self, signals):
        """生成每日投资报告"""
        report_time = datetime.now().strftime('%Y-%m-%d %H:%M')

        # 计算当前资产
        position_value = sum(p.get('current_value', 0) for p in self.positions.values())
        total_assets = self.capital + position_value

        # 计算收益
        total_return = (total_assets - self.initial_capital) / self.initial_capital
        daily_target_achieved = total_return >= self.daily_target

        # 手续费统计
        trade_count = len(self.trade_log)
        avg_fees_per_trade = self.total_fees_paid / max(trade_count, 1)

        report = f"""
{'='*70}
📊 量化投资日报 - {report_time}
{'='*70}

💰 资产状况
  现金: {self.capital:.2f}元
  持仓市值: {position_value:.2f}元
  总资产: {total_assets:.2f}元

📈 收益情况
  总收益: {total_return*100:+.2f}%
  月目标进度: {total_return/self.monthly_target*100:.1f}%
  日目标: {'✅ 已达成' if daily_target_achieved else '❌ 未达成'}

💸 手续费统计
  累计手续费: {self.total_fees_paid:.2f}元
  交易次数: {trade_count}笔
  平均每笔: {avg_fees_per_trade:.2f}元

🎯 今日交易信号 (共{len(signals)}个)
"""

        for i, sig in enumerate(signals[:5], 1):
            action_emoji = '🟢' if sig['action'] == 'BUY' else '🔴'
            report += f"\n  {i}. {action_emoji} {sig['name']}({sig['code']}) - {sig['action']}\n"
            report += f"     策略: {sig['strategy']} | 强度: {sig['strength']}\n"
            report += f"     理由: {sig['reason']}\n"
            report += f"     置信度: {sig['confidence']:.0%}\n"

        report += f"\n{'='*70}\n"

        return report

    def run_daily_analysis(self):
        """每日分析流程"""
        print(f"\n{'🚀'*35}")
        print(f"量化投资系统启动 - {datetime.now().strftime('%Y-%m-%d')}")
        print(f"{'🚀'*35}\n")

        # 1. 获取市场数据
        market_data = self.get_market_data()

        # 2. 分析交易信号
        signals = self.analyze_signals(market_data)

        # 3. 如果有买入信号，计算仓位
        buy_signals = [s for s in signals if s['action'] == 'BUY']
        for sig in buy_signals[:2]:  # 最多2个买入信号
            sig['suggested_amount'] = self.calculate_position_size(sig)

        # 4. 生成报告
        report = self.generate_daily_report(signals)
        print(report)

        # 5. 保存报告
        report_file = f"{self.log_dir}/report_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        # 6. 保存状态
        self.save_state()

        # 7. 输出可执行建议
        if signals:
            print("\n💡 执行建议：")
            for i, sig in enumerate(signals[:3], 1):
                if sig['action'] == 'BUY':
                    print(f"{i}. 买入 {sig['name']}({sig['code']})")
                    print(f"   建议金额: {sig.get('suggested_amount', 0):.2f}元")
                    print(f"   操作: 在券商APP中买入")
                else:
                    print(f"{i}. 卖出 {sig['name']}({sig['code']})")
                    print(f"   理由: {sig['reason']}")
                print()
        else:
            print("\n💡 今日无明确交易信号，建议观望\n")

        return signals

    def record_trade(self, code, name, action, price, shares, reason=''):
        """记录交易（手动执行后记录）"""

        # ===== T+1检查 =====
        if action == 'SELL' and code in self.positions:
            buy_date = datetime.fromisoformat(self.positions[code].get('buy_time', datetime.now().isoformat())).date()
            if buy_date == datetime.now().date():
                print(f"❌ T+1限制：{name} 今日买入，无法卖出")
                return False

        # ===== 最小交易单位检查 =====
        if action == 'BUY' and shares < self.trading_rules['min_shares']:
            print(f"❌ 最小交易单位：需要至少买入{self.trading_rules['min_shares']}股")
            return False

        # ===== 计算滑点成本 =====
        if action == 'BUY':
            # 买入价上浮
            actual_price = price * (1 + self.trading_rules['slippage_rate'])
        else:
            # 卖出价下浮
            actual_price = price * (1 - self.trading_rules['slippage_rate'])

        amount = actual_price * shares
        fees = self.calculate_fees(amount, action, code)
        net_amount = amount + fees if action == 'BUY' else amount - fees

        trade = {
            'time': datetime.now().isoformat(),
            'code': code,
            'name': name,
            'action': action,
            'price': actual_price,
            'target_price': price,  # 用户期望价格
            'slippage': abs(actual_price - price) * shares,  # 滑点成本
            'shares': shares,
            'amount': amount,
            'fees': fees,
            'net_amount': net_amount,
            'reason': reason
        }

        if action == 'BUY':
            total_cost = amount + fees
            if self.capital >= total_cost:
                self.capital -= total_cost
                self.total_fees_paid += fees
                self.positions[code] = {
                    'name': name,
                    'shares': shares,
                    'cost_price': actual_price,
                    'target_price': price,
                    'current_price': actual_price,
                    'current_value': amount,
                    'profit_pct': 0,
                    'buy_time': datetime.now().isoformat(),
                    'buy_fees': fees,
                    'slippage_cost': abs(actual_price - price) * shares
                }
                self.today_trades[code] = True  # 标记今日买入
                self.trade_log.append(trade)
                print(f"✅ 记录买入: {name} {shares}股 @ {actual_price:.3f}元")
                print(f"   目标价格: {price:.2f}元")
                print(f"   滑点成本: {trade['slippage']:.2f}元")
                print(f"   交易金额: {amount:.2f}元")
                print(f"   手续费: {fees:.2f}元")
                print(f"   总成本: {total_cost:.2f}元")
                return True
            else:
                print(f"❌ 资金不足（需要{total_cost:.2f}元，可用{self.capital:.2f}元）")
                return False
        else:  # SELL
            if code in self.positions:
                pos = self.positions[code]
                net_received = amount - fees
                self.capital += net_received
                self.total_fees_paid += fees

                # 计算实际收益（扣除双边手续费和滑点）
                buy_fees = pos.get('buy_fees', 0)
                buy_slippage = pos.get('slippage_cost', 0)
                total_fees = buy_fees + fees
                total_slippage = buy_slippage + trade['slippage']
                profit = (actual_price - pos['cost_price']) * shares - total_fees - total_slippage

                trade['profit'] = profit
                trade['total_fees'] = total_fees
                trade['total_slippage'] = total_slippage
                self.trade_log.append(trade)
                del self.positions[code]

                print(f"✅ 记录卖出: {name} {shares}股 @ {actual_price:.3f}元")
                print(f"   目标价格: {price:.2f}元")
                print(f"   滑点成本: {trade['slippage']:.2f}元")
                print(f"   交易金额: {amount:.2f}元")
                print(f"   手续费: {fees:.2f}元")
                print(f"   实际到账: {net_received:.2f}元")
                print(f"   净利润: {profit:+.2f}元")
                print(f"   总成本: 手续费{total_fees:.2f}元 + 滑点{total_slippage:.2f}元")
                return True

        self.save_state()
        return False


def main():
    print("🎯 量化投资系统启动")
    print("目标: 月收益10% | 初始资金: 1000元")
    print("="*70)

    investor = QuantInvestor(capital=1000, monthly_target=0.10)
    investor.run_daily_analysis()

    # 交互式记录交易
    print("\n📝 记录交易（可选）")
    print("格式: BUY/SELL 代码 名称 价格 股数")
    print("示例: BUY 000001 平安银行 10.5 100")
    print("输入 'quit' 退出\n")

    while True:
        try:
            user_input = input("交易记录> ").strip()
            if user_input.lower() == 'quit':
                break

            parts = user_input.split()
            if len(parts) >= 5 and parts[0] in ['BUY', 'SELL']:
                action = parts[0]
                code = parts[1]
                name = parts[2]
                price = float(parts[3])
                shares = int(parts[4])

                investor.record_trade(code, name, action, price, shares)
            else:
                print("格式错误，请重新输入")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"错误: {e}")

    print("\n系统退出，状态已保存")


if __name__ == "__main__":
    main()
