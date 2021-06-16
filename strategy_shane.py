from load_history import data
import trader

class Shane(trader.Trader):
    def __init__(self):
        super().__init__(self)

    def strategy(self):
        sell_signal_short = 0.2 # percentage diff from above
        sell_signal_long = 1 # percentage diff from
        buy_signal_short = 0.5 # percentage diff from

        if self.ma[5] >= self.ma[7] and self.ma[3] >= sell_signal_short/100 and self.ma[7] >= sell_signal_long/100:
            self.sell()
        elif self.ma[3] >= sell_signal_short/100 and self.ma[7] >= sell_signal_long/100:
            self.sell()
        elif self.ma[5] >= buy_signal_short/100:
            self.buy()

final_value = Shane().run(data, verbose=True)
print(final_value)
