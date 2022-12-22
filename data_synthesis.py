from feature_engineering import FeatureEngineer
from datetime import datetime
from pandas import date_range,DataFrame

class DataSynthesizer:
    def __init__(self,raw_data):
        self.__raw_df = raw_data
        self.__featured_data = self.engineer_features()
    
    @property
    def raw_data(self):
        return self.__raw_df

    @property 
    def featured_data(self):
        return self.__featured_data

    def engineer_features(self) -> DataFrame:
        feature_engineer = FeatureEngineer(self.__raw_df)
        featured_df = feature_engineer.create_features()
        # featured_df.to_excel('featured1.xlsx')
        return featured_df

    def create_testSet(self,start_date,end_date):
        """
        Args:
        start_date (string) : format (yyyy-mm-dd)
        end_date (string) : format (yyyy-mm-dd)
        
        Returns:
        x_train (ndarray (m,n)): m samples with n features
        y_train (ndarray (m,1)): m target values       
        """
        test_start = datetime.strptime(start_date,'%Y-%m-%d')
        test_end = datetime.strptime(end_date,'%Y-%m-%d')
        dates = date_range(start_date,end_date).astype(str)

        df_test = self.featured_data[(test_start<=self.featured_data['date']) & (self.featured_data['date']<test_end)]
        x_test = df_test.iloc[:,1:6].to_numpy()
        y_test = df_test.iloc[:,-1:].to_numpy()
        return x_test,y_test,dates

    def create_trainingSet(self,date):
        """
        Args:
        date (string) : format (yyyy-mm-dd)
        
        Returns:
        x_train (ndarray (m,n)): m samples with n features
        y_train (ndarray (m,1)): m target values       
        """
        df_train = self.featured_data[self.featured_data['date']<=datetime.strptime(date,'%Y-%m-%d')]
        x_train = df_train.iloc[:,1:6].to_numpy()
        y_train = df_train.iloc[:,-1:].to_numpy()      
        return x_train,y_train  
