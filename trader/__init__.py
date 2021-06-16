class Trader():
    def __init__(self, strategy):
        self.bought = False
        self.amountUSD = 100
        self.amountDOGE = 0
        self.current_price = 0
        self.ma = {
            3 : 0,
            5 : 0,
            7 : 0,
            8 : 0,
            15: 0,
            40: 0,
            100: 0,
        }

    def buy(self):
        if self.bought:
            return
        self.amountDOGE = self.amountUSD/self.current_price
        self.amountUSD = 0
        self.bought = True

    def sell(self):
        if not self.bought:
            return
        self.amountUSD = self.amountDOGE*self.current_price
        self.amountDOGE = 0
        self.bought = False

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
            self.current_price = data[i][4]
            self.update_ma(data, i)
            self.strategy()
            if i%100==0 and verbose:
                print(round(self.amountUSD+self.current_price*self.amountDOGE,2))
        return self.amountUSD+self.current_price*self.amountDOGE
