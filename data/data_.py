from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt


class SentiAnal():

    finviz_url = "https://finviz.com/quote.ashx?t="

    def __init__(self,*tickers):
        self.tickers = tickers

        news_tables = {}
        for ticker in tickers:
            url = self.finviz_url + ticker
            req = Request(url=url,headers={'user-agent':'my-app'})
            res = urlopen(req)
            html_response = BeautifulSoup(res,features="html.parser")
            news_table = html_response.find(id='news-table')
            news_tables[ticker] = news_table



        final_data = []

        for ticker,news_data in news_tables.items():
            
            for row in news_data.findAll('tr'):
                news_title = row.a.text
                date_data = row.td.text.split(' ')
        
                if len(date_data) == 1:
                    time = date_data[0]
                else:
                    date = date_data[0]
                    time = date_data[1]

                final_data.append([ticker,date,time,news_title])

            
        df = pd.DataFrame(final_data,columns=['ticker','date','time','news_title'])

        vader = SentimentIntensityAnalyzer()

        func = lambda news_title: vader.polarity_scores(news_title)['compound']

        df['compound'] = df['news_title'].apply(func)

        df['date'] = pd.to_datetime(df.date).dt.date



        mean_df = df.groupby(['ticker','date']).mean()
        mean_df = mean_df.unstack()

        mean_df = mean_df.xs('compound',axis='columns').transpose()

        plt.figure(figsize=(10,8))
        save = mean_df.plot(kind='bar').get_figure()

        savename = ticker+".jpg"
        save.savefig(savename,bbox_inches='tight', dpi=100)


