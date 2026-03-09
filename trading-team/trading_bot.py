#!/usr/bin/env python3
"""
A股交易团队 - 增强版
支持多日运行、自动决策、实时监控
"""

import akshare as ak
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random
import os

class EnhancedTradingTeam:
    def __init__(self, initial_capital=1000, target_multiplier=10, days=30):
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.target = initial_capital * target_multiplier
        self.days_remaining = days
        self.total_days = days
        
        self.positions = {}
        self.trade_log = []
        self.daily_reports = []
        self.win_count = 0
        self.loss_count = 0
        
        # 策略权重（动态调整）
        self.strategy_weights = {
            '打板策略': 0.3,
            '超跌反弹': 0.25,
            '资金博弈': 0.25,
            '龙头战法': 0.2
        }
        
        # 风险参数
        self.max_position_ratio = 0.35  # 提高到35%
        self.stop_loss_ratio = -0.05     # 止损-5%
        self.take_profit_ratio = 0.10    # 止盈10%
        
        # 日志目录
        self.log_dir = "/Users/gesong/.openclaw/workspace/trading-team/logs"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def log(self, role, message):
        """格式化日志输出"""
        icons = {
            '数据分析师': '📊',
            '策略研究员': '🔬',
            '风险控制官': '🛡️',
            '交易执行员': '💼',
            '系统': '🤖'
        }
        icon = icons.get(role, '📌')
        print(f"{icon} [{role}] {message}")
    
    def get_real_time_data(self):
        """获取实时市场数据"""
        self.log('数据分析师', '正在获取市场数据...')
        
        market_data = {
            'limit_up_stocks': [],
            'hot_sectors': [],
            'fund_flow': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 涨停板数据
            limit_up = ak.stock_zt_pool_em(date=datetime.now().strftime("%Y%m%d"))
            if not limit_up.empty:
                market_data['limit_up_stocks'] = limit_up.head(10).to_dict('records')
                self.log('数据分析师', f"今日涨停: {len(limit_up)}只")
        except Exception as e:
            self.log('数据分析师', f"涨停数据获取失败: {e}")
        
        try:
            # 板块数据
            sectors = ak.stock_board_concept_name_em()
            if not sectors.empty:
                market_data['hot_sectors'] = sectors.head(10).to_dict('records')
                self.log('数据分析师', f"热门板块数据已获取")
        except Exception as e:
            self.log('数据分析师', f"板块数据获取失败: {e}")
        
        return market_data
    
    def analyze_candidates(self, market_data):
        """策略分析"""
        self.log('策略研究员', '正在分析候选标的...')
        
        candidates = []
        
        # 策略1: 打板策略
        for stock in market_data.get('limit_up_stocks', [])[:5]:
            try:
                candidates.append({
                    'code': stock['代码'],
                    'name': stock['名称'],
                    'strategy': '打板策略',
                    'reason': f"涨停板，封单强劲",
                    'score': random.uniform(0.7, 0.95),
                    'weight': self.strategy_weights['打板策略']
                })
            except:
                pass
        
        # 策略2: 模拟龙头股（实际应从板块数据筛选）
        hot_stocks = [
            {'code': '000001', 'name': '平安银行', 'score': 0.72},
            {'code': '600519', 'name': '贵州茅台', 'score': 0.68},
            {'code': '000858', 'name': '五粮液', 'score': 0.70}
        ]
        for stock in hot_stocks:
            candidates.append({
                'code': stock['code'],
                'name': stock['name'],
                'strategy': '龙头战法',
                'reason': '板块龙头',
                'score': stock['score'] * random.uniform(0.95, 1.05),
                'weight': self.strategy_weights['龙头战法']
            })
        
        # 策略3: 超跌反弹（模拟）
        oversold = [
            {'code': '002594', 'name': '比亚迪', 'score': 0.65},
            {'code': '300750', 'name': '宁德时代', 'score': 0.63}
        ]
        for stock in oversold:
            candidates.append({
                'code': stock['code'],
                'name': stock['name'],
                'strategy': '超跌反弹',
                'reason': '短期超跌',
                'score': stock['score'] * random.uniform(0.95, 1.05),
                'weight': self.strategy_weights['超跌反弹']
            })
        
        # 综合评分
        for c in candidates:
            c['final_score'] = c['score'] * c['weight']
        
        candidates.sort(key=lambda x: x['final_score'], reverse=True)
        
        self.log('策略研究员', f"筛选出 {len(candidates)} 个候选")
        for i, c in enumerate(candidates[:5], 1):
            print(f"  {i}. {c['name']}({c['code']}) - {c['strategy']} [综合:{c['final_score']:.3f}]")
        
        return candidates
    
    def risk_check(self, decision):
        """风险控制"""
        self.log('风险控制官', '正在审核风险...')
        
        # 检查仓位限制
        if decision['amount'] > self.capital * self.max_position_ratio:
            decision['amount'] = self.capital * self.max_position_ratio
            self.log('风险控制官', f"⚠️ 仓位调整至 {decision['amount']:.2f}元")
        
        # 检查资金充足
        if decision['amount'] > self.capital:
            self.log('风险控制官', '❌ 资金不足')
            return None
        
        # 风险评估
        risk_level = "HIGH" if decision['strategy'] == '打板策略' else "MEDIUM"
        decision['risk_level'] = risk_level
        decision['approved'] = True
        
        self.log('风险控制官', f'✅ 审核通过 [风险:{risk_level}]')
        return decision
    
    def execute_trade(self, decision):
        """执行交易"""
        if not decision or not decision.get('approved'):
            return
        
        self.log('交易执行员', f"执行 {decision['action']}: {decision['name']}")
        
        # 模拟价格（实际应获取实时价格）
        mock_price = random.uniform(10, 50)
        
        if decision['action'] == 'BUY':
            shares = decision['amount'] / mock_price
            self.capital -= decision['amount']
            self.positions[decision['code']] = {
                'name': decision['name'],
                'shares': shares,
                'cost_price': mock_price,
                'current_price': mock_price,
                'strategy': decision['strategy'],
                'buy_time': datetime.now().isoformat()
            }
            
            self.trade_log.append({
                'time': datetime.now().isoformat(),
                'action': 'BUY',
                'code': decision['code'],
                'name': decision['name'],
                'price': mock_price,
                'shares': shares,
                'amount': decision['amount'],
                'strategy': decision['strategy']
            })
            
            self.log('交易执行员', f'✅ 买入成功: {shares:.2f}股 @ {mock_price:.2f}元')
    
    def update_positions(self):
        """更新持仓盈亏"""
        total_profit = 0
        
        for code, pos in self.positions.items():
            # 模拟价格变动
            price_change = random.uniform(-0.03, 0.05)  # -3%到+5%
            pos['current_price'] = pos['cost_price'] * (1 + price_change)
            pos['profit_ratio'] = (pos['current_price'] - pos['cost_price']) / pos['cost_price']
            pos['profit'] = pos['shares'] * (pos['current_price'] - pos['cost_price'])
            total_profit += pos['profit']
        
        return total_profit
    
    def check_stop_loss_take_profit(self):
        """检查止损止盈"""
        to_sell = []
        
        for code, pos in self.positions.items():
            if pos['profit_ratio'] <= self.stop_loss_ratio:
                self.log('风险控制官', f'⚠️ 触发止损: {pos["name"]} ({pos["profit_ratio"]*100:.2f}%)')
                to_sell.append(code)
                self.loss_count += 1
            elif pos['profit_ratio'] >= self.take_profit_ratio:
                self.log('风险控制官', f'✅ 触发止盈: {pos["name"]} ({pos["profit_ratio"]*100:.2f}%)')
                to_sell.append(code)
                self.win_count += 1
        
        for code in to_sell:
            pos = self.positions[code]
            sell_amount = pos['shares'] * pos['current_price']
            self.capital += sell_amount
            
            self.trade_log.append({
                'time': datetime.now().isoformat(),
                'action': 'SELL',
                'code': code,
                'name': pos['name'],
                'price': pos['current_price'],
                'shares': pos['shares'],
                'amount': sell_amount,
                'profit': pos['profit'],
                'reason': '止损' if pos['profit_ratio'] < 0 else '止盈'
            })
            
            del self.positions[code]
    
    def generate_report(self):
        """生成日报"""
        total_profit = self.update_positions()
        total_assets = self.capital + sum(p['shares'] * p['current_price'] for p in self.positions.values())
        progress = (total_assets / self.target) * 100
        
        report = f"""
{'='*60}
📅 交易日报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*60}
💰 资产状况:
   - 现金: {self.capital:.2f}元
   - 持仓市值: {total_assets - self.capital:.2f}元
   - 总资产: {total_assets:.2f}元
   - 今日盈亏: {total_profit:+.2f}元

📊 目标进度:
   - 目标: {self.target:.2f}元
   - 当前进度: {progress:.1f}%
   - 剩余天数: {self.days_remaining}天

📈 交易统计:
   - 持仓数量: {len(self.positions)}
   - 胜率: {self.win_count}/{self.win_count + self.loss_count}
   - 累计交易: {len(self.trade_log)}笔
{'='*60}
"""
        print(report)
        
        # 保存报告
        self.daily_reports.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'capital': self.capital,
            'total_assets': total_assets,
            'progress': progress,
            'positions': self.positions.copy(),
            'trades': len(self.trade_log)
        })
        
        # 保存到文件
        with open(f"{self.log_dir}/daily_report_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(self.daily_reports[-1], f, ensure_ascii=False, indent=2)
        
        return total_assets
    
    def run_daily_cycle(self):
        """每日交易循环"""
        print(f"\n{'🚀'*30}")
        print(f"交易日启动 - 剩余 {self.days_remaining} 天")
        print(f"{'🚀'*30}\n")
        
        # 1. 更新持仓
        self.update_positions()
        
        # 2. 检查止损止盈
        self.check_stop_loss_take_profit()
        
        # 3. 获取市场数据
        market_data = self.get_real_time_data()
        
        # 4. 策略分析
        candidates = self.analyze_candidates(market_data)
        
        # 5. 执行交易（如果有现金）
        if self.capital > 0 and candidates:
            best = candidates[0]
            trade_decision = {
                'code': best['code'],
                'name': best['name'],
                'action': 'BUY',
                'amount': self.capital * 0.8,  # 80%仓位
                'strategy': best['strategy']
            }
            
            approved = self.risk_check(trade_decision)
            if approved:
                self.execute_trade(approved)
        
        # 6. 生成报告
        total_assets = self.generate_report()
        
        # 7. 调整策略权重（基于表现）
        if self.win_count > self.loss_count:
            # 胜率高，保持积极
            pass
        else:
            # 胜率低，降低风险
            self.max_position_ratio = max(0.2, self.max_position_ratio - 0.05)
        
        self.days_remaining -= 1
        
        return total_assets
    
    def run_simulation(self):
        """模拟30天运行"""
        print("🤖 A股交易团队系统启动")
        print(f"目标: {self.days_remaining}天内实现 {self.target:.2f}元 ({self.target/self.initial_capital:.0f}倍收益)\n")
        
        day = 1
        while self.days_remaining > 0:
            print(f"\n{'='*60}")
            print(f"第 {day} 天")
            print(f"{'='*60}")
            
            assets = self.run_daily_cycle()
            
            # 检查是否达成目标
            if assets >= self.target:
                print(f"\n🎉🎉🎉 目标达成！总资产: {assets:.2f}元 🎉🎉🎉")
                break
            
            day += 1
            time.sleep(0.1)  # 模拟间隔
        
        # 最终报告
        print(f"\n{'='*60}")
        print("📊 最终总结")
        print(f"{'='*60}")
        print(f"初始资金: {self.initial_capital:.2f}元")
        print(f"最终资产: {assets:.2f}元")
        print(f"收益率: {(assets/self.initial_capital - 1)*100:.1f}%")
        print(f"总交易: {len(self.trade_log)}笔")
        print(f"胜率: {self.win_count}/{self.win_count + self.loss_count}")
        
        # 保存完整日志
        with open(f"{self.log_dir}/full_log.json", 'w') as f:
            json.dump({
                'initial_capital': self.initial_capital,
                'final_assets': assets,
                'return_rate': (assets/self.initial_capital - 1)*100,
                'trades': self.trade_log,
                'daily_reports': self.daily_reports
            }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    team = EnhancedTradingTeam(
        initial_capital=1000,
        target_multiplier=10,
        days=30
    )
    team.run_simulation()
