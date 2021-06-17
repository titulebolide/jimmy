import trader
import datetime as dt

data = trader.load_history("VETUSDT-1m-data.csv",dt.datetime(2021,5,1), dt.datetime(2021,6,1))

class Hold(trader.Trader):
    def __init__(self):
        super().__init__(self)

    def strategy(self):
        self.buy()

final_value = Hold().run(data, verbose=False)
print(final_value)
