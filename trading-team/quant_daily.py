#!/usr/bin/env python3
"""
量化投资系统 - 定时任务版
每日自动运行，输出交易信号
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quant_investor import QuantInvestor
from datetime import datetime

def main():
    """每日运行的主函数"""
    print(f"\n{'='*70}")
    print(f"量化投资系统 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    # 创建投资者实例
    investor = QuantInvestor(capital=1000, monthly_target=0.10)
    
    # 运行分析
    signals = investor.run_daily_analysis()
    
    # 返回信号数量（用于脚本判断）
    return len(signals)

if __name__ == "__main__":
    signal_count = main()
    print(f"\n✅ 分析完成，生成 {signal_count} 个交易信号")
    print(f"详细报告: investment_logs/report_{datetime.now().strftime('%Y%m%d')}.txt\n")
