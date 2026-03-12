#!/usr/bin/env python3
"""
边界模型策略 (Boundary Model Strategy)

参数定义：
- py = H * 0.28  # 基准价格
- 上边界 = py + 150
- 下边界 = H - 120

使用场景：
- 价格突破上边界 → 卖出信号
- 价格跌破下边界 → 买入信号
- 价格在边界内 → 持有/观望
"""

from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class BoundaryModel:
    """边界模型类"""
    H: float  # 高度值（通常是价格高值或波动幅度）
    
    @property
    def py(self) -> float:
        """基准价格 = H * 0.28"""
        return self.H * 0.28
    
    @property
    def upper_boundary(self) -> float:
        """上边界 = py + 150"""
        return self.py + 150
    
    @property
    def lower_boundary(self) -> float:
        """下边界 = H - 120"""
        return self.H - 120
    
    @property
    def boundary_width(self) -> float:
        """边界宽度"""
        return self.upper_boundary - self.lower_boundary


def get_signal(
    current_price: float,
    H: float,
    tolerance: float = 0.0
) -> tuple[Literal["买入", "卖出", "观望"], str]:
    """
    根据当前价格和边界模型生成交易信号
    
    Args:
        current_price: 当前价格
        H: 高度值
        tolerance: 容差（可选，用于避免微小波动触发信号）
    
    Returns:
        (信号类型, 详细说明)
    """
    model = BoundaryModel(H)
    
    upper = model.upper_boundary
    lower = model.lower_boundary
    py = model.py
    
    if current_price >= upper - tolerance:
        return "卖出", f"价格 {current_price:.2f} 触及上边界 {upper:.2f} (py={py:.2f})"
    elif current_price <= lower + tolerance:
        return "买入", f"价格 {current_price:.2f} 触及下边界 {lower:.2f} (H={H:.2f})"
    else:
        return "观望", f"价格 {current_price:.2f} 在边界内 [{lower:.2f}, {upper:.2f}]"


def calculate_model(H: float) -> dict:
    """
    计算完整的边界模型参数
    
    Args:
        H: 高度值
    
    Returns:
        包含所有参数的字典
    """
    model = BoundaryModel(H)
    return {
        "H": H,
        "py": model.py,
        "上边界": model.upper_boundary,
        "下边界": model.lower_boundary,
        "边界宽度": model.boundary_width
    }


# 测试用例
if __name__ == "__main__":
    print("=" * 60)
    print("边界模型策略测试")
    print("=" * 60)
    
    # 测试1：计算模型参数
    H = 1000
    params = calculate_model(H)
    print(f"\n【测试1】H = {H}")
    for key, value in params.items():
        print(f"  {key}: {value:.2f}")
    
    # 测试2：生成交易信号
    print("\n【测试2】交易信号测试")
    test_prices = [300, 500, 700, 900]
    for price in test_prices:
        signal, detail = get_signal(price, H)
        print(f"  价格 {price}: {signal} - {detail}")
    
    # 测试3：真实案例模拟
    print("\n【测试3】真实案例")
    H_real = 2500
    print(f"  H = {H_real}")
    params_real = calculate_model(H_real)
    for key, value in params_real.items():
        print(f"    {key}: {value:.2f}")
    
    # 模拟几个价格点
    prices = [
        params_real["下边界"],
        params_real["py"],
        params_real["上边界"],
        600  # 中间价格
    ]
    print("\n  信号测试：")
    for p in prices:
        signal, detail = get_signal(p, H_real)
        print(f"    {detail} → {signal}")
