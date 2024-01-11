import backtrader as bt
from datetime import datetime
import yfinance as yf
import pandas as pd
import quantstats
import webbrowser

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close,period = 21)

    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            return 
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY: 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'SELL: 주가 {order.executed.price:,.0f}, '
                         f'수량 {order.executed.size:,.0f}, '
                         f'수수료 {order.executed.comm:,.0f}, '
                         f'자산 {cerebro.broker.getvalue():,.0f}')
            self.bar_executed = len(self)   # ????
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELED')
        elif order.status in [order.margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy()
        else:
            if self.rsi > 70:
                self.sell()
    
    def log(self,txt,dt = None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
data = bt.feeds.PandasData(dataname=yf.download("036570.KS", 
                                               start="2017-01-01", 
                                               end="2019-12-1"))

cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission = 0.0014)
cerebro.addsizer(bt.sizers.PercentSizer,percents = 90)
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')

print(f'Initial Portfolio Value: {cerebro.broker.getvalue():,.0f} KRW')
results = cerebro.run()

# OPEN BACKTEST RESULTS
strat = results[0]
portfolio_stats = strat.analyzers.getbyname('PyFolio')
returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
returns.index = returns.index.tz_convert(None)
quantstats.reports.html(returns, output='stats.html', title='RSI_SMA')
html_file_path = r"C:\Users\ewp\Desktop\mySite\cra_backtest\stats.html"

# Open the HTML file in the default web browser
webbrowser.open(html_file_path)

# PLOT 
print(f'Final Portfolio Value: {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot(style = 'candlestick')
