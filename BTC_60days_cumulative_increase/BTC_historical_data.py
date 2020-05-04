from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

URL = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20200503'#coinmarketcap中比特币数据从2013年4月28日开始有记录
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results= soup.find('div', class_='cmc-table__table-wrapper-outer').find('thead')

clounms_name=[th.text for th in results.tr.find_all('th')]

rows_d=soup.find_all('tr', class_='cmc-table-row')
data_rows=[]
for tr in rows_d:
    rows=[td.text for td in tr.find_all('td')]
    data_rows.append(rows)

df =pd.DataFrame(data_rows,columns=clounms_name)
del df['High']
data=df[['Date','Open*']]

data1=pd.DataFrame(columns=['Date','Open*'])
for x in range(len(data)):
    data1=data1.append(data.iloc[-(x+1)])
data1=data1.reset_index(drop=True)

data1['Open*']=data1['Open*'].str.replace(',','').astype(float)

increase=[0]
for i in range(1,len(data1)):
    si_increase=(data1.loc[i]['Open*']-data1.loc[i-1]['Open*'])/data1.loc[i-1]['Open*']*100
    si_increase=si_increase.round(4)
    increase.append(si_increase)
data1['Single_day_Increase(%)']=increase

sixty_days_increase = [0.00]*59
for i in range(59,len(data1)):
    sixty_days_in=data1.loc[i-59:i]['Single_day_Increase(%)']
    sixty_days_in=sum(sixty_days_in)
    sixty_days_increase.append(sixty_days_in)
sixty_days_increase
data1['Sixty_Days_Increase(%)']=sixty_days_increase

data1['Date']=data1['Date'].str.replace(',','')
data1['Date']=pd.to_datetime(data1['Date'])
data1['Date']=data1['Date'].dt.date

data1.to_csv('BTC_price_history.csv')

data_plt=df[['Date','Sixty_Days_Increase(%)']]
data_plt=data_plt[59:]
data_plt.plot(kind='line', x='Date', y='Sixty_Days_Increase(%)', ax= plt.gca(), grid=True,figsize = (20,10))
plt.savefig('BTC_Sixty_Days_Increase.png')
plt.show()