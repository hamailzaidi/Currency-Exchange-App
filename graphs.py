import pandas as pd
from datetime import datetime

class Graph():
    def __init__(self,history_table_df):
        self.__daily_data = [[x for x in history_table_df['date']],[y for y in history_table_df['usd_price']]]
        
        self.__weekly_avg,self.__monthly_avg = self.group_data(history_table_df)
        
    @property
    def daily_data(self):
        return self.__daily_data
    @property
    def weekly_avg(self):
        return self.__weekly_avg
    @property
    def monthly_avg(self):
        return self.__monthly_avg
    
    def group_data(self,df):
        df['week'] = pd.to_datetime(df.date).dt.strftime("%Y-%U")
        weekly_series = df.groupby('week')['usd_price'].mean()
        weekly_avg = [list(weekly_series.index),list(weekly_series)]

        df['month'] = pd.to_datetime(df.date).dt.strftime("%Y-%m")
        monthly_series = df.groupby('month')['usd_price'].mean()
        monthly_avg = [list(monthly_series.index),list(monthly_series)]

        return weekly_avg,monthly_avg
        