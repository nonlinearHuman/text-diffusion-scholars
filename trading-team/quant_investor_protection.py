    def check_capital_protection(self):
        """检查本金保护机制"""
        # 计算当前总资产
        position_value = sum(p.get('current_value', 0) for p in self.positions.values())
        total_assets = self.capital + position_value
        
        # 计算本金状况
        profit = total_assets - self.initial_capital
        profit_pct = profit / self.initial_capital
        
        status = {
            'total_assets': total_assets,
            'cash': self.capital,
            'position_value': position_value,
            'profit': profit,
            'profit_pct': profit_pct,
            'status': 'NORMAL',
            'warning': None
        }
        
        # 检查熔断线（本金开始亏损）
        if total_assets < self.risk_config['circuit_breaker']:
            status['status'] = 'CIRCUIT_BREAKER'
            status['warning'] = '🚨 熔断线触发：本金开始亏损！立即停止交易！'
            self.log('风险管理', f"🚨 熔断线触发！总资产{total_assets:.2f}元 < 本金{self.initial_capital}元")
            return status
        
        # 检查危险线（本金亏损>5%）
        if total_assets < self.risk_config['danger_line']:
            status['status'] = 'DANGER'
            status['warning'] = '⚠️ 危险线触发：本金亏损>5%，建议清仓观望'
            self.log('风险管理', f"⚠️ 危险线触发！总资产{total_assets:.2f}元")
            return status
        
        # 检查预警线（本金亏损>10%）
        if total_assets < self.risk_config['warning_line']:
            status['status'] = 'WARNING'
            status['warning'] = '⚠️ 预警线触发：本金接近亏损，谨慎操作'
            self.log('风险管理', f"⚠️ 预警线触发！总资产{total_assets:.2f}元")
            return status
        
        return status
    
    def calculate_position_size(self, signal):
        """计算仓位（本金保护模式）"""
        self.log('风险管理', '计算仓位...')
        
        # 检查本金保护状态
        capital_status = self.check_capital_protection()
        
        if capital_status['status'] == 'CIRCUIT_BREAKER':
            self.log('风险管理', '🚨 熔断线触发，禁止买入')
            return 0
        
        if capital_status['status'] == 'DANGER':
            self.log('风险管理', '⚠️ 危险线触发，建议持有现金')
            return 0
        
        # 本金保护模式：更保守的仓位控制
        # 基础仓位降低到25%
        base_position = 0.25
        
        # 根据信号强度调整
        if signal['strength'] == 'STRONG':
            position_ratio = min(0.3, base_position * 1.2)  # 最大30%
        else:
            position_ratio = base_position * 0.8  # 弱信号减仓到20%
        
        # 计算金额
        amount = self.capital * position_ratio
        
        # 必须保留20%现金
        min_cash = self.capital * self.capital_protection['min_cash_reserve']
        if self.capital - amount < min_cash:
            amount = self.capital - min_cash
        
        # 最小交易金额检查
        if amount < self.capital_protection['min_trade_amount']:
            self.log('风险管理', f"❌ 交易金额{amount:.2f}元 < 最小要求{self.capital_protection['min_trade_amount']}元")
            return 0
        
        # ===== 使用盘口价格（卖一价） =====
        price = signal.get('ask_price', signal.get('price', 10.0))
        shares = int(amount / price)
        
        # 调整到100股整数倍
        shares = (shares // self.trading_rules['min_shares']) * self.trading_rules['min_shares']
        
        if shares < self.trading_rules['min_shares']:
            self.log('风险管理', f"❌ 资金不足：最多买{shares}股，不足{self.trading_rules['min_shares']}股")
            return 0
        
        # 重新计算实际金额（使用卖一价）
        amount = shares * price
        
        # ===== 预留手续费（买入+卖出双边） =====
        buy_fees = self.calculate_fees(amount, 'BUY', signal['code'])
        sell_amount = amount * 1.03
        sell_fees = self.calculate_fees(sell_amount, 'SELL', signal['code'])
        total_fees = buy_fees + sell_fees
        
        # ===== 考虑滑点成本 =====
        slippage_cost = amount * self.trading_rules['slippage_rate'] * 2
        
        # ===== 考虑盘口价差 =====
        spread_ratio = signal.get('spread_ratio', 0)
        spread_cost = amount * spread_ratio
        
        # 总成本
        total_cost = amount + buy_fees + slippage_cost + spread_cost
        
        if total_cost > self.capital - min_cash:
            # 减少股数
            shares = int((self.capital - min_cash - buy_fees - slippage_cost - spread_cost) / price)
            shares = (shares // self.trading_rules['min_shares']) * self.trading_rules['min_shares']
            if shares < self.trading_rules['min_shares']:
                return 0
            amount = shares * price
        
        # 计算保本涨幅
        total_trading_cost = total_fees + slippage_cost + spread_cost
        breakeven_pct = total_trading_cost / amount
        
        self.log('风险管理', f"建议仓位: {amount:.2f}元 ({shares}股 @ {price:.2f}元)")
        self.log('风险管理', f"保留现金: {self.capital - amount:.2f}元 ({(self.capital - amount)/self.capital*100:.1f}%)")
        self.log('风险管理', f"双边总成本: {total_trading_cost:.2f}元（需涨{breakeven_pct*100:.2f}%回本）")
        
        # 本金保护警告
        if capital_status['status'] == 'WARNING':
            self.log('风险管理', f"⚠️ 预警状态：本金接近亏损，建议谨慎操作")
        
        signal['suggested_shares'] = shares
        signal['suggested_price'] = price * (1 + self.trading_rules['slippage_rate'])
        signal['breakeven_pct'] = breakeven_pct
        signal['spread_cost'] = spread_cost
        signal['capital_status'] = capital_status
        
        return amount