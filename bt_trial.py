import backtrader as bt
import yfinance as yf

class MyStrategy(bt.Strategy):
    def __init__(self):
        super().__init__()
        self.rsi = bt.indicators.RSI(self.data.close)

    def next(self):
        if not self.position:
            if self.rsi[0] < 30:
                self.buy()
        else:
            if self.rsi[0] > 70:
                self.sell()

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

data = bt.feeds.PandasData(dataname=yf.download("MSFT", 
                                               start="2018-01-01", 
                                               end="2018-12-31"))

cerebro.adddata(data)

cerebro.broker.setcash(10000)

# CHECK: sizers?
cerebro.addsizer(bt.sizers.SizerFix, stake=30)

print(f'Initial Portfolio Value: {cerebro.broker.getvalue():,.0f} USD')

# Run the strategy
cerebro.run()

# Generate a plot
cerebro.plot()