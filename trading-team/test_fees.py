#!/usr/bin/env python3
"""测试手续费计算"""

import sys
sys.path.insert(0, '/Users/gesong/.openclaw/workspace/trading-team')

from quant_investor import QuantInvestor

def test_fees():
    print("=" * 70)
    print("测试手续费计算")
    print("=" * 70)
    
    investor = QuantInvestor(capital=1000)
    
    # 测试不同金额的手续费
    test_cases = [
        (1000, 'BUY', '000001', '平安银行'),
        (1000, 'SELL', '000001', '平安银行'),
        (500, 'BUY', '600519', '贵州茅台'),
        (500, 'SELL', '600519', '贵州茅台'),
        (100, 'BUY', '000858', '五粮液'),
        (100, 'SELL', '000858', '五粮液'),
    ]
    
    for amount, action, code, name in test_cases:
        fees = investor.calculate_fees(amount, action, code)
        print(f"\n{action} {name}({code}) - 金额:{amount}元")
        print(f"  手续费: {fees:.2f}元")
        print(f"  费率: {fees/amount*100:.3f}%")
    
    # 测试实际交易
    print("\n" + "=" * 70)
    print("模拟交易测试")
    print("=" * 70)
    
    investor.record_trade('000001', '平安银行', 'BUY', 10.0, 50)
    print(f"剩余资金: {investor.capital:.2f}元")
    
    investor.record_trade('000001', '平安银行', 'SELL', 10.5, 50)
    print(f"剩余资金: {investor.capital:.2f}元")
    print(f"累计手续费: {investor.total_fees_paid:.2f}元")

if __name__ == "__main__":
    test_fees()
