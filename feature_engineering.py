class FeatureEngineer:
    def __init__(self,df):
        self.df = df
        
    def create_features(self):
        self.select_window(2)
        self.add_simple_moving_average(3)
        self.add_simple_moving_average(7)
        self.create_outputs()
        self.df.dropna(inplace=True)
        return self.df
    
    def add_simple_moving_average(self,days):
        self.df[f'{days}days_avg'] = self.df['usd_price'].rolling(days).mean().round(2)
    
    def select_window(self,days):
        for i in range(days):
            self.df[f'{i+1}dayback_price'] = self.df['usd_price'].shift(periods=i+1)
    
    def create_outputs(self):
        self.df['nextday_price'] = self.df['usd_price'].shift(periods=-1)