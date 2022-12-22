from bs4 import BeautifulSoup 
import requests
from pandas import DataFrame
from datetime import datetime 
from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

class Scrapper:
    
    def __init__(self):
        self.__scrapping_link = config.get('Scrapper','usd_data_link')
        self.__live_price_link = config.get('Scrapper','live_usd_price_link')
        soup = self.__get_website_soup(self.__scrapping_link)
        self.__scrapped_data = self.__extract_data(soup)
        self.__history = self.__create_historyTable()
    
    @property 
    def scrapping_link(self):
        return self.__scrapping_link
    
    @property 
    def live_price_link(self):
        return self.__live_price_link
    
    @property
    def scrapped_data(self):
        return self.__scrapped_data
    @property
    def history_table(self):
        return self.__history

    
    def __get_website_soup(self,page_url:str) -> BeautifulSoup:
        pgcontent = requests.get(page_url,verify=False).content
        soup = BeautifulSoup(pgcontent,'html.parser')
        return soup
    
    def __extract_data(self,soup:BeautifulSoup) -> DataFrame:
        total_data = int(float(config.get('Scrapper','training_years')) * 365)
        tr = soup.find_all('tr')
        lis = []
        for i in range(1,total_data):
            d = {}
            d["date"] = datetime.strptime(tr[i].find_all('td')[1].text,'%d/%m/%Y')
            if d["date"] == datetime(2022,7,29):            #catering two anamolies
                d['usd_price'] = 239.0
            elif d["date"] == datetime(2022,9,18):
                d['usd_price'] = 237.0
            else:
                d['usd_price'] = round(float(tr[i].find_all('td')[3].text.replace(' PKR','')),2)
            lis.append(d)   
        df = DataFrame(reversed(lis))
        return df


    def usd_price_now(self) -> float:
        soup = self.__get_website_soup(self.__live_price_link)
        try:
            usd_val = soup.find_all('tr',{'class':'colone'})[2].find('strong').text
            return float(usd_val)
        except:
            return 0

    def __create_historyTable(self) -> DataFrame:
        total_data = int(float(config.get('Scrapper','history_table_months')) * 30)
        history_df = self.__scrapped_data.iloc[-total_data:].reset_index().drop(['index'],axis=1)
        history_df['day'] = history_df['date'].dt.strftime('%A')
        history_df['date'] = history_df['date'].astype(str) 
        history_df['pkr_price'] = round(1/history_df['usd_price'],5)
        return history_df
