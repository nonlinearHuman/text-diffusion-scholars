#!/usr/bin/env python3
"""测试P0级风险过滤"""

import sys
sys.path.insert(0, '/Users/gesong/.openclaw/workspace/trading-team')

from quant_investor import QuantInvestor

def test_p0_risks():
    print("=" * 70)
    print("测试P0级风险过滤")
    print("=" * 70)
    
    investor = QuantInvestor(capital=1100)
    
    # 获取市场数据
    print("\n【测试1】获取市场数据（含ST股票和停牌股票）")
    market_data = investor.get_market_data()
    
    print(f"数据时间: {market_data.get('data_timestamp', 'N/A')}")
    print(f"数据延迟: {market_data.get('data_delay_seconds', 0)}秒")
    print(f"股票数量: {len(market_data['hot_stocks'])}")
    
    # 分析信号
    print("\n【测试2】分析交易信号（应自动过滤ST和停牌）")
    signals = investor.analyze_signals(market_data)
    
    print(f"\n有效信号数量: {len(signals)}")
    for i, sig in enumerate(signals[:3], 1):
        print(f"\n{i}. {sig['name']}({sig['code']}) - {sig['action']}")
        print(f"   策略: {sig['strategy']}")
        print(f"   价格: 卖一{sig.get('ask_price', 0):.3f}元 / 买一{sig.get('bid_price', 0):.3f}元")
        print(f"   盘口价差: {sig.get('spread_ratio', 0)*100:.2f}%")
        print(f"   板块: {sig.get('board_type', 'MAIN')}")
        if sig['action'] == 'BUY':
            investor.calculate_position_size(sig)
            print(f"   保本涨幅: {sig.get('breakeven_pct', 0)*100:.2f}%")
    
    # 测试买入ST股票（应被拒绝）
    print("\n【测试3】尝试买入ST股票（应被过滤）")
    st_found = any(s.get('is_st', False) for s in market_data['hot_stocks'])
    print(f"数据中包含ST股票: {st_found}")
    print(f"信号中包含ST股票: {any('ST' in s['name'] for s in signals)}")
    
    # 测试买入停牌股票（应被拒绝）
    print("\n【测试4】尝试买入停牌股票（应被过滤）")
    suspended_found = any(s.get('is_suspended', False) for s in market_data['hot_stocks'])
    print(f"数据中包含停牌股票: {suspended_found}")
    print(f"信号中包含停牌股票: {any('停牌' in s['name'] for s in signals)}")

if __name__ == "__main__":
    test_p0_risks()
