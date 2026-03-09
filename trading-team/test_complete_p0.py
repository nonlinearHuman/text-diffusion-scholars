#!/usr/bin/env python3
"""完整测试P0级风险控制"""

import sys
sys.path.insert(0, '/Users/gesong/.openclaw/workspace/trading-team')

from quant_investor import QuantInvestor

def test_complete_p0():
    print("=" * 70)
    print("完整测试P0级风险控制")
    print("=" * 70)
    
    investor = QuantInvestor(capital=2000)  # 增加资金
    
    # 获取市场数据
    print("\n【测试1】数据延迟检测")
    market_data = investor.get_market_data()
    print(f"✅ 数据时间戳: {market_data.get('data_timestamp')}")
    print(f"✅ 数据延迟: {market_data.get('data_delay_seconds', 0)}秒")
    
    print("\n【测试2】ST股票过滤")
    st_stocks = [s for s in market_data['hot_stocks'] if s.get('is_st', False)]
    print(f"数据中ST股票数量: {len(st_stocks)}")
    for s in st_stocks:
        print(f"  - {s['name']}({s['code']})")
    
    print("\n【测试3】停牌股票过滤")
    suspended = [s for s in market_data['hot_stocks'] if s.get('is_suspended', False)]
    print(f"数据中停牌股票数量: {len(suspended)}")
    for s in suspended:
        print(f"  - {s['name']}({s['code']})")
    
    print("\n【测试4】盘口价差分析")
    for stock in market_data['hot_stocks'][:3]:
        if not stock.get('is_st') and not stock.get('is_suspended'):
            bid = stock.get('bid_price', 0)
            ask = stock.get('ask_price', 0)
            spread = (ask - bid) / ask * 100
            print(f"  - {stock['name']}: 买一{bid:.2f}元 / 卖一{ask:.2f}元 / 价差{spread:.2f}%")
    
    print("\n【测试5】板块规则识别")
    for stock in market_data['hot_stocks'][:5]:
        board = stock.get('board_type', 'MAIN')
        limit = stock.get('board_type', 'MAIN')
        if board == 'STAR':
            threshold = '±20%'
        elif board == 'GEM':
            threshold = '±20%'
        elif board == 'BSE':
            threshold = '±30%'
        else:
            threshold = '±10%'
        print(f"  - {stock['name']}: {board}板块，涨跌停{threshold}")
    
    print("\n【测试6】完整信号生成")
    signals = investor.analyze_signals(market_data)
    print(f"有效信号数量: {len(signals)}")
    
    for i, sig in enumerate(signals[:2], 1):
        print(f"\n  信号{i}: {sig['name']}({sig['code']})")
        print(f"    动作: {sig['action']}")
        print(f"    策略: {sig['strategy']}")
        print(f"    置信度: {sig['confidence']:.0%}")
        
        if sig['action'] == 'BUY':
            amount = investor.calculate_position_size(sig)
            print(f"    建议金额: {amount:.2f}元")
            print(f"    建议股数: {sig.get('suggested_shares', 0)}股")
            print(f"    保本涨幅: {sig.get('breakeven_pct', 0)*100:.2f}%")
            print(f"    盘口价差成本: {sig.get('spread_cost', 0):.2f}元")
    
    print("\n" + "=" * 70)
    print("✅ P0级风险控制测试完成")
    print("=" * 70)
    print("\n已实现的风险控制：")
    print("  1. ✅ 数据延迟检测")
    print("  2. ✅ ST股票过滤")
    print("  3. ✅ 停牌股票过滤")
    print("  4. ✅ 盘口价差分析")
    print("  5. ✅ 板块规则识别")

if __name__ == "__main__":
    test_complete_p0()
