class Trader():
    def __init__(self, fees = 0):
        self.bought = False
        self.amountFIAT = 100
        self.amountCOIN = 0
        self.current_price = 0
        self.fees = fees # percentage
        ma_keys = [1,2,3,4,5,6,7,8,9,10,15,40,100]
        self.start_index = max(ma_keys) + 1
        self.ma = {i:0 for i in ma_keys}
        self.data_index = self.start_index
        self.no_trades = 0

    def buy(self):
        if self.bought:
            return
        self.amountCOIN = self.amountFIAT/self.current_price*(1-self.fees/100)
        self.amountFIAT = 0
        self.bought = True
        self.no_trades += 1

    def sell(self):
        if not self.bought:
            return
        self.amountFIAT = self.amountCOIN*self.current_price*(1-self.fees/100)
        self.amountCOIN = 0
        self.bought = False
        self.no_trades += 1

    def update_ma(self, data, i):
        for length in self.ma.keys():
            self.ma[length] = (data[i][4] - data[i-length][4])/data[i-length][4]
        return
        for length in self.ma.keys():
            ma_c = self.ma[length]
            price_to_remove = 0
            if i-length >= 0:
                price_to_remove = data[i-length][4]
            self.ma[length] = (ma_c*length - price_to_remove + data[i][4])/length

    def strategy(self):
        pass #do nothing

    def run(self, data, verbose = True):
        for i in range(101, len(data)):
            self.data_index = i
            self.current_price = data[i][4]
            self.update_ma(data, i)
            self.strategy()
            if i%100==0 and verbose:
                amount = round(self.amountFIAT+self.current_price*self.amountCOIN, 2)
                amount_no_trade = round(100/data[self.start_index][4]*data[i][4], 2)
                print(f"""
{str(data[i][0])} :
    Holding : {amount}
    If you were not trading : {amount_no_trade} ({round((amount-amount_no_trade)/amount_no_trade*100,2)} %)
    Nb of trades : {self.no_trades}
                """)
        return self.amountFIAT+self.current_price*self.amountCOIN
