#!/usr/bin/env python3
"""测试新增因素"""

import sys
sys.path.insert(0, '/Users/gesong/.openclaw/workspace/trading-team')

from quant_investor import QuantInvestor

def test_new_factors():
    print("=" * 70)
    print("测试新增交易因素")
    print("=" * 70)
    
    investor = QuantInvestor(capital=1100)  # 增加资金避免资金不足
    
    # 测试1: T+1限制
    print("\n【测试1】T+1交易限制")
    print("买入平安银行...")
    success = investor.record_trade('000001', '平安银行', 'BUY', 10.0, 100)
    if success:
        print("\n尝试当日卖出（应该失败）...")
        investor.record_trade('000001', '平安银行', 'SELL', 10.5, 100)
    
    # 清空持仓
    investor.positions = {}
    investor.today_trades = {}
    investor.capital = 1100
    
    # 测试2: 最小交易单位
    print("\n【测试2】最小交易单位（100股）")
    print("尝试买入50股（应该失败）...")
    investor.record_trade('000001', '平安银行', 'BUY', 10.0, 50)
    
    # 测试3: 滑点成本
    print("\n【测试3】滑点成本")
    print("买入100股@10.0元（含滑点）...")
    success = investor.record_trade('000001', '平安银行', 'BUY', 10.0, 100)
    if success and '000001' in investor.positions:
        print(f"实际成本价: {investor.positions['000001']['cost_price']:.3f}元")
        print(f"滑点成本: {investor.positions['000001']['slippage_cost']:.2f}元")
        
        # 模拟第二天（绕过T+1）
        from datetime import datetime, timedelta
        investor.positions['000001']['buy_time'] = (datetime.now() - timedelta(days=1)).isoformat()
        
        # 测试4: 总成本分析
        print("\n【测试4】完整交易成本分析")
        print("卖出100股@10.5元（含滑点）...")
        investor.record_trade('000001', '平安银行', 'SELL', 10.5, 100)
        print(f"最终资金: {investor.capital:.2f}元")
        print(f"收益率: {(investor.capital - 1100) / 1100 * 100:.2f}%")
        print(f"累计手续费: {investor.total_fees_paid:.2f}元")

if __name__ == "__main__":
    test_new_factors()
