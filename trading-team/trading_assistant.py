#!/usr/bin/env python3
"""
人机协作交易系统
定期检查并推送交易信号
"""

import json
from datetime import datetime, time
import os

class TradingAssistant:
    def __init__(self):
        self.state_file = "/Users/gesong/.openclaw/workspace/trading-team/investment_logs/state.json"
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                self.capital = data.get('capital', 1000)
                self.positions = data.get('positions', {})
                self.trade_log = data.get('trade_log', [])
        else:
            self.capital = 1000
            self.positions = {}
            self.trade_log = []
    
    def save_state(self):
        """保存状态"""
        with open(self.state_file, 'w') as f:
            json.dump({
                'capital': self.capital,
                'positions': self.positions,
                'trade_log': self.trade_log,
                'updated': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def check_trading_time(self):
        """检查是否在交易时段"""
        now = datetime.now().time()
        morning = time(9, 30) <= now <= time(11, 30)
        afternoon = time(13, 0) <= now <= time(15, 0)
        return morning or afternoon
    
    def get_total_assets(self):
        """计算总资产"""
        position_value = sum(
            pos.get('shares', 0) * pos.get('current_price', pos.get('cost_price', 0))
            for pos in self.positions.values()
        )
        return self.capital + position_value
    
    def check_risk_status(self):
        """检查风险状态"""
        total = self.get_total_assets()
        
        if total < 1000:
            return 'CIRCUIT_BREAKER', '🚨 熔断线触发：本金开始亏损！'
        elif total < 1050:
            return 'DANGER', '⚠️ 危险线触发：本金亏损>5%'
        elif total < 1100:
            return 'WARNING', '⚠️ 预警线触发：本金接近亏损'
        else:
            return 'NORMAL', '✅ 正常'
    
    def update_from_user_feedback(self, action, code, name, price, shares, success, current_capital=None):
        """根据用户反馈更新状态"""
        if success:
            if action == 'BUY':
                self.capital -= price * shares
                self.positions[code] = {
                    'name': name,
                    'shares': shares,
                    'cost_price': price,
                    'current_price': price,
                    'buy_time': datetime.now().isoformat()
                }
                print(f"✅ 已记录买入：{name} {shares}股 @ {price}元")
                
            elif action == 'SELL':
                if code in self.positions:
                    del self.positions[code]
                    self.capital += price * shares
                    print(f"✅ 已记录卖出：{name} {shares}股 @ {price}元")
            
            if current_capital:
                self.capital = current_capital
            
            self.save_state()
            return True
        else:
            print(f"❌ 交易未执行：{action} {name}")
            return False
    
    def generate_signal_report(self):
        """生成交易信号报告"""
        risk_status, risk_msg = self.check_risk_status()
        total = self.get_total_assets()
        
        report = f"""
🔔 交易信号 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

【账户状态】
- 现金：{self.capital:.2f}元
- 持仓市值：{total - self.capital:.2f}元
- 总资产：{total:.2f}元
- 风险状态：{risk_msg}

【持仓情况】
"""
        
        if self.positions:
            for code, pos in self.positions.items():
                profit_pct = (pos.get('current_price', pos['cost_price']) - pos['cost_price']) / pos['cost_price']
                report += f"- {pos['name']}({code}): {pos['shares']}股 @ {pos['cost_price']:.2f}元, 盈亏{profit_pct*100:+.2f}%\n"
        else:
            report += "- 无持仓\n"
        
        report += f"""
【本金保护】
- 距预警线：{total - 1100:+.2f}元
- 距危险线：{total - 1050:+.2f}元
- 距熔断线：{total - 1000:+.2f}元
"""
        
        return report, risk_status

def main():
    assistant = TradingAssistant()
    
    # 生成当前状态报告
    report, risk_status = assistant.generate_signal_report()
    print(report)
    
    # 如果是危险或熔断状态，特别提示
    if risk_status in ['DANGER', 'CIRCUIT_BREAKER']:
        print("\n🚨 严重警告：本金保护线已触发！")
        print("建议：立即停止交易，持有现金观望")

if __name__ == "__main__":
    main()
