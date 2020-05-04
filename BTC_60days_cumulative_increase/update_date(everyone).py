from datetime import date
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

todaysdate =date.today().strftime('%Y-%m-%d')#返回今天的时间

URL = 'https://coinmarketcap.com/currencies/bitcoin/'
page = requests.get(URL) #向网页发起请求，
soup = BeautifulSoup(page.content, 'html.parser')#解析网站
results= soup.find('span', class_='cmc-details-panel-price__price')#找到需要爬取的数据
btc_price=results.text #获取文本
btc_price=btc_price.replace(',','').replace('$','')#比特币价格转换为浮点数
btc_price=float(btc_price)


df=pd.read_csv('BTC_price_history.csv')

Single_day_Increase=(btc_price- df.iloc[-1]['Open*'])/df.iloc[-1]['Open*']*100#计算今天的单日涨幅
Single_day_Increase=round(Single_day_Increase,4)

sixty_days=df.iloc[-59:]['Single_day_Increase(%)']
Sixty_Days_Increase=sum(sixty_days)+Single_day_Increase#计算今天的累计涨幅

data=pd.DataFrame({'Date':[todaysdate],'Open*':[btc_price],'Single_day_Increase(%)':[Single_day_Increase],'Sixty_Days_Increase(%)':[Sixty_Days_Increase]})
df=df.append(data)
df.to_csv('BTC_price_history.csv',index=False)#将今天的数据添加到原表中

data_plt=df[['Date','Sixty_Days_Increase(%)']]
data_plt=data_plt[59:]
data_plt.plot(kind='line', x='Date', y='Sixty_Days_Increase(%)', ax= plt.gca(), grid=True,figsize = (20,10))
plt.savefig('BTC_Sixty_Days_Increase.png')
plt.show()