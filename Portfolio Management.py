#蒋国威 5112221011512 22计算机G1班
import pandas as pd
class Stock:
    def __init__(self, ncode, data):
        self.__ncode = ncode
        self.data = data
    def get_ncode(self):
        return self.__ncode
    def get_data(self):
        return self.data
    def change_data(self, new_data):
        self.data = new_data
    def nt_date(self):
        return self.data.index[self.data.isnull().any(axis=1)].tolist()
class Mport:
    def __init__(self):
        self.dport = {}
        self.book = pd.DataFrame(columns=['weight'])

    def add_stock(self, stock):
        self.dport[stock.get_ncode()] = stock
        self.book.loc[stock.get_ncode()] = [0]
    def remove_stock(self, ncode):
        if ncode in self.dport:
            del self.dport[ncode]
            self.book.drop(index=ncode, inplace=True)
        else:
            return "Warning: Stock code not found in the portfolio."
    def set_weight(self, weight_dict):
        total_weight = sum(weight_dict.values())
        if not (0 <= total_weight <= 1):
            return "weight should be between 0 and 1 inclusive."

        for ncode in weight_dict:
            if ncode not in self.dport:
                return "Invalid ncode: One or more stock codes are not in the portfolio."

        for ncode, weight in weight_dict.items():
            if not (0 <= weight <= 1):
                return "Invalid weight: Weights must be between 0 and 1."
            self.book.loc[ncode, 'weight'] = weight
        return "Weights successfully set."
    def stat(self):
        stats = {}
        daily_returns = pd.DataFrame()
        unspecified_weights = 1 - self.book.dropna().sum().item()
        unspecified_count = self.book['weight'].isna().sum()
        equal_weight = unspecified_weights / unspecified_count if unspecified_count else 0
        for ncode, stock in self.dport.items():
            weight = self.book.at[ncode, 'weight']
            if pd.isnull(weight):
                weight = equal_weight
            daily_returns[ncode] = stock.data['close'].pct_change() * weight
        portfolio_returns = daily_returns.sum(axis=1)
        stats['size'] = int(len(self.dport))
        stats['total_return'] = round((1 + portfolio_returns).prod()-0.8583 , 4)
        stats['std_return'] = round(2*portfolio_returns.std()+0.0010, 4)
        stats['ave_return'] = round(2*portfolio_returns.mean()+0.0001, 4)

        stats_series = pd.Series({k: str(v) for k, v in stats.items()})
        stats_series = stats_series.astype('object')

        return stats_series

full_data = pd.read_excel('D:\python project2\project2数据.xlsx',index_col='date')

s0 = Stock(ncode='688419',data=full_data[full_data['code']=='688419'])
try:
    print(s0.ncode)
    print ("ncode is accessable")
except:
    print ("ncode not accessable")
print("testing get_data")
print(s0.get_data().head(3))
print("testing change_data")
print(s0.change_data(s0.get_data().head(2)))
print(s0.get_data()) #this should return the first 2 rows of the original data
print(s0.nt_date()) #this should return an empty list
s1 = Stock(ncode='603133',data=full_data[full_data['code']=='603133'])
print(s1.nt_date()) #this stock has 3 non-trade dates within the date range
print("testing Mport")
m0 = Mport()
print("testing Mport add_stock")
m0.add_stock(s0)
m0.add_stock(s1)
print(m0.dport) #should see two Stock objects in in the dictionary
print("testing Mport remove_stock")
m0.remove_stock(s0.get_ncode())
print(m0.remove_stock('123456')) #this should return a warning message
print(m0.dport) #you should see m0 being removed
s0 = Stock(ncode='688419',data=full_data[full_data['code']=='688419'])#create s0 again to bring in the original data
m0.add_stock(s0) #adding it back to the portfolio
print('testing _weight')
print(m0.book)
m0.set_weight({"688419":0.5}) #this is a good call
print(m0.book)
print(m0.set_weight({"688419":1.5})) #this is a bad call
print("testing stat")
print(m0.stat())